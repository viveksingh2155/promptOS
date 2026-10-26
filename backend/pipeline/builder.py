import os
import ollama
import json
import re
import asyncio
from pipeline.language import build_language_instruction

# Configure Ollama client with environment variable
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CLIENT = ollama.Client(host=OLLAMA_BASE_URL)

BUILDER_SYSTEM_GPT = """You are an expert prompt architect specializing in GPT. Restructure into Role, Task, Requirements, Format sections.
Return ONLY valid JSON:
{
  "structured_prompt": "...",
  "sections": [{"label": "Role", "content": "..."}, ...]
}
"""

def _call_ollama(model: str, messages: list, temperature: float = 0.3) -> str:
    try:
        response = OLLAMA_CLIENT.chat(model=model, messages=messages, options={"temperature": temperature})
        return response["message"]["content"].strip()
    except Exception as e:
        raise ConnectionError(f"Ollama connection failed at {OLLAMA_BASE_URL}. Error: {str(e)}")

async def build(cleaned_text: str, analysis: dict, fmt: str = "gpt", model: str = "llama3.1", target_lang: str = "original") -> dict:
    context = f"Cleaned prompt: {cleaned_text}\nFormat: {fmt}"
    try:
        language_instruction = build_language_instruction(cleaned_text, target_lang)
        content = await asyncio.to_thread(
            _call_ollama, model,
            [{"role": "system", "content": BUILDER_SYSTEM_GPT + "\n\n" + language_instruction},
             {"role": "user", "content": f"Build: {context}"}],
            0.3
        )
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        return json.loads(json_match.group()) if json_match else {}
    except ConnectionError:
        raise
    except Exception as e:
        return {"structured_prompt": cleaned_text, "error": str(e)}
