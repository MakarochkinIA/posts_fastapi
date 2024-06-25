import redis

from redis import asyncio as aioredis

from app.core.config import settings


async def aredis_client():
    try:
        return await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding="utf8", decode_responses=True
        )
    except redis.exceptions.ConnectionError as e:
        print("Connection error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


def redis_client():
    try:
        return redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding="utf8", decode_responses=True
        )
    except redis.exceptions.ConnectionError as e:
        print("Connection error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
