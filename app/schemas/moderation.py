from pydantic import BaseModel
from typing import Optional

class ModerationRequest(BaseModel):
    text: str
    user_id: str
    context: Optional[str] = None

class ModerationResponse(BaseModel):
    is_flagged: bool
    category: str
    cleaned_text: Optional[str] = None
    explanation: Optional[str] = None
    source: str
    confidence: str
