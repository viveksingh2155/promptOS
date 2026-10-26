import os
import ollama
import json
import re
import asyncio
from pipeline.language import build_language_instruction

# Configure Ollama client with environment variable
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CLIENT = ollama.Client(host=OLLAMA_BASE_URL)

ANALYZER_SYSTEM = """You are an expert prompt analyzer. Your job is to analyze a user's raw prompt and extract structured metadata.
Return ONLY valid JSON with this exact structure:
{
  "intent": "brief description of what the user wants",
  "entities": ["list", "of", "key", "entities"],
  "complexity": 0.0,
  "warnings": ["any issues with the prompt"],
  "target_domain": "domain/topic area",
  "clarity_score": 0
}
"""

def _call_ollama(model: str, messages: list, temperature: float = 0.1) -> str:
    try:
        response = OLLAMA_CLIENT.chat(model=model, messages=messages, options={"temperature": temperature})
        return response["message"]["content"].strip()
    except Exception as e:
        raise ConnectionError(f"Ollama connection failed at {OLLAMA_BASE_URL}. Ensure Ollama is running and accessible. Error: {str(e)}")

async def analyze(prompt: str, model: str = "llama3.1", target_lang: str = "original") -> dict:
    try:
        language_instruction = build_language_instruction(prompt, target_lang)
        content = await asyncio.to_thread(
            _call_ollama, model,
            [{"role": "system", "content": ANALYZER_SYSTEM + "\n\n" + language_instruction},
             {"role": "user", "content": f"Analyze this prompt:\n\n{prompt}"}],
            0.1
        )
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        return json.loads(json_match.group()) if json_match else {}
    except ConnectionError:
        raise
    except Exception as e:
        return {"error": str(e)}
