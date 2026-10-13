import re
import json
from app.data.profanity_wordlist import PROFANITY_WORDS

def fast_path_filter(text: str):
    # Check for URLs
    if re.search(r"http[s]?://", text):
        return {
            "is_flagged": True,
            "category": "spam",
            "cleaned_text": text,
            "explanation": "Contains a URL pattern",
            "source": "rule_based",
            "confidence": "high"
        }

    # Check for profanity
    for word in PROFANITY_WORDS:
        if word in text.lower():
            cleaned = text.lower().replace(word, "******")
            return {
                "is_flagged": True,
                "category": "profanity",
                "cleaned_text": cleaned,
                "explanation": f"Contains a Hinglish profanity term: {word}",
                "source": "rule_based",
                "confidence": "high"
            }

    # If clean
    return {
        "is_flagged": False,
        "category": "clean",
        "cleaned_text": text,
        "explanation": "No issues detected",
        "source": "rule_based",
        "confidence": "high"
    }
