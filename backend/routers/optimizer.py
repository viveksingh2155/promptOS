import asyncio
import json
import time
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
from schemas import OptimizeRequest
import models
from pipeline.analyzer import analyze
from pipeline.cleaner import clean
from pipeline.builder import build
from pipeline.optimizer import optimize

router = APIRouter()

async def pipeline_generator(prompt: str, fmt: str, model: str, target_lang: str, db: Session):
    """SSE generator that runs the 4-agent pipeline and streams events."""
    def event(data: dict) -> str:
        return f"data: {json.dumps(data)}\n\n"

    total_start = time.time()

    try:
        # Detect language upfront
        from pipeline.language import detect_input_language
        detected_lang = detect_input_language(prompt)

        # Stream detected language info immediately
        yield event({
            "type": "language_detected",
            "detectedLanguage": detected_lang,
            "targetLanguage": target_lang
        })

        # Analyzer Agent
        yield event({"type": "step_start", "step": "analyzer", "timestamp": time.time()})
        yield event({"type": "progress", "progress": 5, "eta": "~12s"})
        t0 = time.time()
        analysis = await analyze(prompt, model=model, target_lang=target_lang)
        
        if "error" in analysis:
            raise Exception(f"Analyzer error: {analysis['error']}")
        
        analyzer_ms = int((time.time() - t0) * 1000)
        yield event({
            "type": "step_complete",
            "step": "analyzer",
            "result": json.dumps(analysis),
            "duration": analyzer_ms,
            "preview": f"Intent: {analysis.get('intent', '')[:60]}",
            "timestamp": time.time(),
        })
        yield event({"type": "progress", "progress": 25, "eta": "~9s"})

        # Cleaner Agent
        yield event({"type": "step_start", "step": "cleaner", "timestamp": time.time()})
        t0 = time.time()
        cleaned = await clean(prompt, analysis, model=model, target_lang=target_lang)
        
        if "error" in cleaned:
            raise Exception(f"Cleaner error: {cleaned['error']}")
        
        cleaner_ms = int((time.time() - t0) * 1000)
        cleaned_text = cleaned.get("cleaned_text", prompt)
        yield event({
            "type": "step_complete",
            "step": "cleaner",
            "result": cleaned_text,
            "duration": cleaner_ms,
            "preview": f"Removed: {', '.join(cleaned.get('removed_items', [])[:2])}",
            "timestamp": time.time(),
        })
        yield event({"type": "progress", "progress": 50, "eta": "~6s"})

        # Builder Agent
        yield event({"type": "step_start", "step": "builder", "timestamp": time.time()})
        t0 = time.time()
        built = await build(cleaned_text, analysis, fmt, model=model, target_lang=target_lang)
        
        if "error" in built:
            raise Exception(f"Builder error: {built['error']}")
        
        builder_ms = int((time.time() - t0) * 1000)
        structured = built.get("structured_prompt", cleaned_text)
        sections = built.get("sections", [])
        yield event({
            "type": "step_complete",
            "step": "builder",
            "result": structured,
            "duration": builder_ms,
            "preview": structured[:80],
            "timestamp": time.time(),
        })
        yield event({"type": "progress", "progress": 75, "eta": "~3s"})

        # Optimizer Agent
        yield event({"type": "step_start", "step": "optimizer", "timestamp": time.time()})
        t0 = time.time()
        optimized = await optimize(structured, sections, analysis, model=model, target_lang=target_lang)
        
        if "error" in optimized:
            raise Exception(f"Optimizer error: {optimized['error']}")
        
        optimizer_ms = int((time.time() - t0) * 1000)

        final_prompt = optimized.get("optimized_prompt", structured)
        score = optimized.get("score", 75)
        clarity_score = optimized.get("clarity_score", 75)
        context_score = optimized.get("context_score", 75)
        token_count = optimized.get("token_estimate", len(final_prompt.split()))
        gen_time = optimized.get("generation_time", optimizer_ms)
        diff_segments = optimized.get("diff_segments", [{"text": final_prompt, "type": "unchanged"}])
        tags = optimized.get("tags", [])

        yield event({
            "type": "step_complete",
            "step": "optimizer",
            "result": final_prompt[:80],
            "duration": optimizer_ms,
            "preview": f"Score: {score}/100",
            "timestamp": time.time(),
        })
        yield event({"type": "progress", "progress": 100, "eta": "Done"})

        # Save to database
        history_id = str(uuid.uuid4())
        title = prompt[:60] + ("..." if len(prompt) > 60 else "")
        total_ms = int((time.time() - total_start) * 1000)

        db_item = models.PromptHistory(
            id=history_id,
            title=title,
            original_prompt=prompt,
            optimized_prompt=final_prompt,
            score=score,
            clarity_score=clarity_score,
            context_score=context_score,
            token_count=token_count,
            model=model,
            format=fmt,
            latency=float(total_ms),
            has_hallucination_risk=score < 50,
            detected_language=detected_lang,
            target_language=target_lang,
        )
        db.add(db_item)
        db.commit()

        result = {
            "optimizedPrompt": final_prompt,
            "originalPrompt": prompt,
            "score": score,
            "clarityScore": clarity_score,
            "contextScore": context_score,
            "tokenCount": token_count,
            "generationTime": gen_time,
            "diffHighlights": diff_segments,
            "sections": sections,
            "tags": tags,
            "detectedLanguage": detected_lang,
            "targetLanguage": target_lang,
        }
        yield event({"type": "complete", "result": result})
        
    except ConnectionError as e:
        # Ollama connection issues
        yield event({
            "type": "error", 
            "message": f"AI service unavailable: {str(e)}. Please ensure Ollama is running and accessible."
        })
    except Exception as e:
        # General pipeline errors
        yield event({
            "type": "error",
            "message": f"Pipeline error: {str(e)}"
        })

@router.post("/optimize")
async def optimize_prompt(request: OptimizeRequest, db: Session = Depends(get_db)):
    """
    Optimize a prompt through the 4-agent AI pipeline.
    Streams progress events via Server-Sent Events (SSE).
    """
    return StreamingResponse(
        pipeline_generator(request.prompt, request.format, request.model, request.target_lang, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
