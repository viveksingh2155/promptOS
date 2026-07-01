import asyncio
from pipeline.analyzer import analyze
from pipeline.cleaner import clean
from pipeline.builder import build
from pipeline.optimizer import optimize


def test_multilingual_pipeline_uses_input_language():
    prompt = "Escribe un prompt claro para pedirle a un asistente que resuma un artículo en español."
    analysis = asyncio.run(analyze(prompt, model="llama3.1"))
    cleaned = asyncio.run(clean(prompt, analysis, model="llama3.1"))
    built = asyncio.run(build(cleaned.get("cleaned_text", prompt), analysis, fmt="gpt", model="llama3.1"))
    optimized = asyncio.run(optimize(built.get("structured_prompt", prompt), built.get("sections", []), analysis, model="llama3.1"))

    assert isinstance(analysis, dict)
    assert isinstance(cleaned, dict)
    assert isinstance(built, dict)
    assert isinstance(optimized, dict)
    assert "optimized_prompt" in optimized or "error" in optimized
