from typing import AsyncGenerator
from datetime import datetime
import json
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import async_session
from models.conversation import Conversation
from models.message import Message
from services.rag_service import RagService
from services.memory_service import MemoryService
from ai.ollama_client import OllamaClient
from utils.logger import get_logger

logger = get_logger(__name__)

class ChatService:
    def __init__(self, ollama: OllamaClient, rag: RagService, memory: MemoryService, redis, db_session_factory):
        self.ollama = ollama
        self.rag = rag
        self.memory = memory
        self.redis = redis
        self.db_session_factory = db_session_factory

    async def process_message(
        self,
        user_id: str,
        conversation_id: str,
        message: str,
        model: str = "llama3.2",
        use_rag: bool = True,
        use_memory: bool = True,
        stream: bool = True
    ) -> AsyncGenerator[str, None]:
        conv = await self._get_or_create_conversation(user_id, conversation_id)
        user_msg = Message(conversation_id=conv.id, role="user", content=message)
        async with self.db_session_factory() as db:
            db.add(user_msg)
            await db.commit()

        rag_context = ""
        if use_rag:
            docs = await self.rag.retrieve(message, user_id, top_k=5)
            if docs:
                rag_context = "\n\n".join(docs)
        memory_context = ""
        if use_memory:
            memory_context = await self.memory.get_context(user_id, message)

        system = self._build_prompt(rag_context, memory_context)
        generator = self.ollama.stream_chat(system, message, model)

        full_response = ""
        async for chunk in generator:
            full_response += chunk
            yield chunk

        assistant_msg = Message(conversation_id=conv.id, role="assistant", content=full_response)
        async with self.db_session_factory() as db:
            db.add(assistant_msg)
            await db.commit()

        if use_memory:
            await self.memory.store(user_id, message, full_response)

        await self.redis.setex(f"conv:{conv.id}:messages", 3600, json.dumps([user_msg.content, assistant_msg.content]))

    def _build_prompt(self, rag_context: str, memory_context: str) -> str:
        prompt = "Du bist Twilight AI, ein professioneller, hilfsbereiter KI-Assistent. Antworte präzise und freundlich."
        if rag_context:
            prompt += f"\n\nVerwende diese Dokumente als Kontext:\n{rag_context}"
        if memory_context:
            prompt += f"\n\nBerücksichtige frühere Informationen:\n{memory_context}"
        return prompt

    async def _get_or_create_conversation(self, user_id: str, conv_id: str) -> Conversation:
        async with self.db_session_factory() as db:
            conv = await db.get(Conversation, conv_id)
            if not conv:
                conv = Conversation(id=conv_id, user_id=user_id, title="Neues Gespräch")
                db.add(conv)
                await db.commit()
                await db.refresh(conv)
            return conv
