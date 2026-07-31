import json
from datetime import datetime
from core.redis_client import redis_pool

class MemoryService:
    def __init__(self, redis):
        self.redis = redis

    async def get_context(self, user_id: str, query: str, limit: int = 3) -> str:
        key = f"memory:{user_id}"
        data = await self.redis.get(key)
        if not data:
            return ""
        items = json.loads(data)
        relevant = [item["content"] for item in items[-limit:]]
        return "\n".join(relevant)

    async def store(self, user_id: str, question: str, answer: str):
        key = f"memory:{user_id}"
        current = await self.redis.get(key)
        memories = json.loads(current) if current else []
        memories.append({"question": question, "content": answer, "timestamp": datetime.utcnow().isoformat()})
        if len(memories) > 100:
            memories = memories[-100:]
        await self.redis.setex(key, 86400 * 30, json.dumps(memories))
