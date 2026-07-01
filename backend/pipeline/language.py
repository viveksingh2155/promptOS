import re

HINGLISH_WORDS = {
    "kya", "kaise", "likho", "batao", "samjhao", "karo", "gaya", "gayi", "karna", "krna",
    "ho", "hai", "haan", "nhi", "nahin", "nahi", "ko", "se", "aur", "toh", "hi", "bhi",
    "tum", "aap", "mera", "meri", "mujhe", "tujhe", "hum", "humein", "unhe", "unko",
    "karne", "krne", "chal", "chalo", "baat", "kuch", "sab", "ab", "kab", "tab", "jab",
    "rha", "raha", "rhi", "rahi", "rhe", "rahe", "hoga", "hogi", "hoge", "tha", "thi",
    "the", "karlo", "karo", "dekh", "dekho", "bhejo", "nikalo", "banao", "create-karo",
    "website-banao", "code-likho", "batana", "samajh", "aata", "aati", "aate", "sakte",
    "sakta", "sakti", "milega", "milegi"
}

LANG_MAP = {
    'en': 'English',
    'hi': 'Hindi',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'ja': 'Japanese',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'zh': 'Chinese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'ru': 'Russian',
    'pt': 'Portuguese',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'th': 'Thai',
    'el': 'Greek',
    'vi': 'Vietnamese',
    'pl': 'Polish'
}

def is_hinglish(prompt: str) -> bool:
    """Detect if prompt is Hinglish (Hindi written in Latin script)."""
    # Find all alphabetic word characters
    words = re.findall(r'[a-zA-Z]+', prompt.lower())
    if not words:
        return False
    
    hinglish_count = sum(1 for w in words if w in HINGLISH_WORDS)
    # If we have multiple Hinglish keywords, or more than 20% of words are Hinglish
    return hinglish_count >= 2 or (len(words) > 3 and (hinglish_count / len(words)) >= 0.2)

def detect_input_language(prompt: str) -> str:
    """Return a simple language label using a hybrid NLP approach."""
    if not prompt or not prompt.strip():
        return "English"

    # 1. Check scripts using unicode blocks
    if re.search(r'[\u0900-\u097F]', prompt):
        return "Hindi"
    if re.search(r'[\u0600-\u06FF]', prompt):
        return "Arabic"
    if re.search(r'[\u3040-\u30FF\u31F0-\u31FF]', prompt):
        return "Japanese"
    if re.search(r'[\uAC00-\uD7AF]', prompt):
        return "Korean"
    if re.search(r'[\u4E00-\u9FFF]', prompt):
        # Could be Chinese or Japanese Kanji
        if not re.search(r'[\u3040-\u30FF\u31F0-\u31FF]', prompt):
            return "Chinese"
        return "Japanese"
    if re.search(r'[\u0E00-\u0E7F]', prompt):
        return "Thai"
    if re.search(r'[\u0370-\u03FF]', prompt):
        return "Greek"
    if re.search(r'[\u0400-\u04FF]', prompt):
        return "Russian"

    # 2. Check Hinglish keywords
    if is_hinglish(prompt):
        return "Hinglish"

    # 3. Use langdetect for standard texts
    try:
        from langdetect import detect
        code = detect(prompt)
        return LANG_MAP.get(code, "English")
    except Exception:
        # Fallback to English if langdetect fails
        return "English"

def build_language_instruction(prompt: str, target_lang: str = "original") -> str:
    """Return a prompt instruction that guides optimization to match target_lang."""
    detected = detect_input_language(prompt)
    
    target_lang_clean = (target_lang or "original").lower().strip()
    
    if target_lang_clean == "original":
        if detected == "Hinglish":
            return (
                "IMPORTANT: The user prompt is in Hinglish (Hindi written in Latin script). "
                "Keep the final output in the same Hinglish style (Hindi words in Latin characters) so the user can read it. "
                "Do NOT write in Devnagari Hindi characters unless explicitly asked."
            )
        return (
            f"IMPORTANT: Preserve the user's original language. "
            f"The final output must be in {detected} (the language of the input prompt). "
            f"Do NOT translate it to any other language unless explicitly requested by the user."
        )
    else:
        # Translate to target language
        target_name = target_lang_clean.capitalize()
        if target_lang_clean in ["hi", "hindi"]:
            target_name = "Hindi (in Devnagari script)"
        elif target_lang_clean in ["en", "english"]:
            target_name = "English"
        elif target_lang_clean in ["es", "spanish"]:
            target_name = "Spanish"
        elif target_lang_clean in ["fr", "french"]:
            target_name = "French"
        elif target_lang_clean in ["de", "german"]:
            target_name = "German"
        elif target_lang_clean in ["it", "italian"]:
            target_name = "Italian"
        elif target_lang_clean in ["ja", "japanese"]:
            target_name = "Japanese"
        elif target_lang_clean in ["zh", "chinese"]:
            target_name = "Chinese"
        elif target_lang_clean in ["ar", "arabic"]:
            target_name = "Arabic"
        
        return (
            f"IMPORTANT: The final output MUST be in {target_name}. "
            f"Translate and adapt the prompt content completely to {target_name} while optimizing. "
            f"Ensure all JSON values, headings, role instructions, task instructions, and text are in {target_name}."
        )
