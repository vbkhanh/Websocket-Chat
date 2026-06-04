
import json
import redis.asyncio as redis
from app.settings import settings

class RedisPubSub:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def publish(self, channel: str, message: dict):
        await self.redis.publish(channel, json.dumps(message))

    async def subscribe(self, channel: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        return pubsub
