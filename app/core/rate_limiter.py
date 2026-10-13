from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Rate limiter setup
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT}/minute"]
)
