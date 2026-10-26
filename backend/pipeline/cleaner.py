import os
import ollama
import json
import re
import asyncio
from pipeline.language import build_language_instruction

# Configure Ollama client with environment variable
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CLIENT = ollama.Client(host=OLLAMA_BASE_URL)

CLEANER_SYSTEM = """You are an expert prompt cleaner.
Return ONLY valid JSON:
{
  "cleaned_text": "the cleaned version of the prompt",
  "removed_items": ["list of what was removed/fixed"],
  "clarity_delta": 0
}
"""

def _call_ollama(model: str, messages: list, temperature: float = 0.2) -> str:
    try:
        response = OLLAMA_CLIENT.chat(model=model, messages=messages, options={"temperature": temperature})
        return response["message"]["content"].strip()
    except Exception as e:
        raise ConnectionError(f"Ollama connection failed at {OLLAMA_BASE_URL}. Error: {str(e)}")

async def clean(prompt: str, analysis: dict, model: str = "llama3.1", target_lang: str = "original") -> dict:
    context = f"Original prompt: {prompt}\nIntent: {analysis.get('intent', '')}"
    try:
        language_instruction = build_language_instruction(prompt, target_lang)
        content = await asyncio.to_thread(
            _call_ollama, model,
            [{"role": "system", "content": CLEANER_SYSTEM + "\n\n" + language_instruction},
             {"role": "user", "content": f"Clean this prompt:\n\n{context}"}],
            0.2
        )
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        return json.loads(json_match.group()) if json_match else {}
    except ConnectionError:
        raise
    except Exception as e:
        return {"cleaned_text": prompt, "error": str(e)}
