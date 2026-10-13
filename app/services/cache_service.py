import redis
import json
from app.core.config import settings

# Redis client
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_cached_result(text: str):
    key = f"moderation:{hash(text)}"
    result = redis_client.get(key)
    if result:
        return json.loads(result)
    return None

def set_cached_result(text: str, result: dict):
    key = f"moderation:{hash(text)}"
    redis_client.set(key, json.dumps(result), ex=3600)  # 1 hour expiry
