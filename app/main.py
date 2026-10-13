from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.api import moderation

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Hinglish Moderation API")

# Middleware for rate limiting
app.state.limiter = limiter

# Include moderation route
app.include_router(moderation.router, prefix="/api/v1")
