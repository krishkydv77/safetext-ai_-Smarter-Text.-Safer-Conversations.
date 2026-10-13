import json
from app.services.cache_service import get_cached_result, set_cached_result
from app.services.fast_path import fast_path_filter
from app.services.gemini_service import call_gemini

async def run_pipeline(text: str, user_id: str, context: str = None):
    # 1. Cache check
    cached = get_cached_result(text)
    if cached:
        return cached

    # 2. Fast-path rules
    result = fast_path_filter(text)
    if result["category"] in ["clean", "spam", "profanity"]:
        set_cached_result(text, result)
        return result

    # 3. Gemini fallback
    gemini_result = call_gemini(text)
    parsed = json.loads(gemini_result)
    parsed["source"] = "gemini_llm"
    parsed["confidence"] = "high"

    set_cached_result(text, parsed)
    return parsed
