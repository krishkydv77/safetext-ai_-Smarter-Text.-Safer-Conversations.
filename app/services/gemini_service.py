from google.genai import Client
from app.core.config import settings

client = Client(api_key=settings.GEMINI_API_KEY)

def call_gemini(text: str):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"""
        Classify the following Hinglish text into categories:
        clean | profanity | spam | harassment | other.
        Also return a cleaned version with bad words masked.

        Text: "{text}"
        Respond in strict JSON with fields:
        is_flagged, category, cleaned_text, explanation, source, confidence
        """
    )
    return response.text
