from typing import List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ai_memory import AIMemory, AIRecommendation, AIConversation, AIConversationMessage


class AIRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_memory(self, mem: AIMemory):
        self.session.add(mem)
        await self.session.flush()
        return mem

    async def list_memories(self, user_id, limit=50, offset=0) -> Tuple[List[AIMemory], int]:
        q = select(AIMemory).where(AIMemory.user_id == user_id).order_by(AIMemory.created_at.desc())
        total_q = select(func.count()).select_from(AIMemory).where(AIMemory.user_id == user_id)
        total = (await self.session.execute(total_q)).scalar_one()
        res = await self.session.execute(q.limit(limit).offset(offset))
        return res.scalars().all(), total

    async def create_conversation(self, conv: AIConversation):
        self.session.add(conv)
        await self.session.flush()
        return conv

    async def add_message(self, msg: AIConversationMessage):
        self.session.add(msg)
        await self.session.flush()
        return msg
