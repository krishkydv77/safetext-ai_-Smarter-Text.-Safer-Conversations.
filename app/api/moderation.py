from fastapi import APIRouter, Request
from app.schemas.moderation import ModerationRequest, ModerationResponse
from app.services.moderation_pipeline import run_pipeline

router = APIRouter()

@router.post("/moderate", response_model=ModerationResponse)
async def moderate_text(request: Request, body: ModerationRequest):
    """
    Hinglish moderation endpoint
    """
    result = await run_pipeline(body.text, body.user_id, body.context)
    return result
