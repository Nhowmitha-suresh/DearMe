from typing import List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.journal import JournalEntry


class JournalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entry: JournalEntry):
        self.session.add(entry)
        await self.session.flush()
        return entry

    async def get(self, entry_id):
        q = select(JournalEntry).where(JournalEntry.id == entry_id)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def list_by_user(self, user_id, limit=50, offset=0) -> Tuple[List[JournalEntry], int]:
        q = select(JournalEntry).where(JournalEntry.user_id == user_id).order_by(JournalEntry.created_at.desc())
        total_q = select(func.count()).select_from(JournalEntry).where(JournalEntry.user_id == user_id)
        total = (await self.session.execute(total_q)).scalar_one()
        res = await self.session.execute(q.limit(limit).offset(offset))
        return res.scalars().all(), total
