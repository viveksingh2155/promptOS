import os
import ollama
import json
import re
import asyncio
import time
from pipeline.language import build_language_instruction

# Configure Ollama client with environment variable
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CLIENT = ollama.Client(host=OLLAMA_BASE_URL)

OPTIMIZER_SYSTEM = """Evaluate prompt quality, clarity, and return score (0-100) and optimized version.
Return JSON:
{
  "optimized_prompt": "...",
  "score": 90,
  "clarity_score": 90,
  "context_score": 90
}
"""

def _call_ollama(model: str, messages: list, temperature: float = 0.2) -> str:
    try:
        response = OLLAMA_CLIENT.chat(model=model, messages=messages, options={"temperature": temperature})
        return response["message"]["content"].strip()
    except Exception as e:
        raise ConnectionError(f"Ollama connection failed at {OLLAMA_BASE_URL}. Error: {str(e)}")

async def optimize(structured_prompt: str, sections: list, analysis: dict, model: str = "llama3.1", target_lang: str = "original") -> dict:
    t0 = time.time()
    try:
        language_instruction = build_language_instruction(structured_prompt, target_lang)
        content = await asyncio.to_thread(
            _call_ollama, model,
            [{"role": "system", "content": OPTIMIZER_SYSTEM + "\n\n" + language_instruction},
             {"role": "user", "content": f"Optimize:\n\n{structured_prompt}"}],
            0.2
        )
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        res = json.loads(json_match.group()) if json_match else {}
        res["generation_time"] = int((time.time() - t0) * 1000)
        return res
    except ConnectionError:
        raise
    except Exception as e:
        return {"optimized_prompt": structured_prompt, "error": str(e)}
