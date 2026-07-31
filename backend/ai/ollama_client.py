import aiohttp
import json
from typing import AsyncGenerator, List

class OllamaClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def stream_chat(self, system: str, user: str, model: str = "llama3.2") -> AsyncGenerator[str, None]:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "stream": True
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/api/chat", json=payload) as resp:
                async for line in resp.content:
                    if line:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]

    async def embed(self, text: str) -> List[float]:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/api/embeddings", json={"model": "nomic-embed-text", "prompt": text}) as resp:
                data = await resp.json()
                return data.get("embedding", [])
