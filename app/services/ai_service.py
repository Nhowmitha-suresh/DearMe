from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.ai_repository import AIRepository
from app.models.ai_memory import AIMemory, AIConversation, AIConversationMessage
from typing import Tuple


class AIService:
    def __init__(self, session: AsyncSession):
        self.repo = AIRepository(session)

    async def store_memory(self, user, memory_type, content, metadata=None, embedding_id=None):
        mem = AIMemory(user_id=user.id, memory_type=memory_type, content=content, metadata=metadata or {}, embedding_id=embedding_id)
        await self.repo.create_memory(mem)
        return mem

    async def start_conversation(self, user, topic=None):
        conv = AIConversation(user_id=user.id, topic=topic)
        await self.repo.create_conversation(conv)
        return conv

    async def add_message(self, conversation, sender, message, metadata=None):
        msg = AIConversationMessage(conversation_id=conversation.id, sender=sender, message=message, metadata=metadata or {})
        await self.repo.add_message(msg)
        return msg
