import redis.asyncio as redis
import json

from config import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


async def get_cache(key: str):
    value = await redis_client.get(key)
    if value:
        return json.loads(value)
    return None


async def set_cache(key: str, value, ex=60):
    await redis_client.set(key, json.dumps(value), ex=ex)


async def delete_cache(key: str):
    await redis_client.delete(key)
