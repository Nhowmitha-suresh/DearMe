from typing import List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.mood import MoodLog


class MoodRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, log: MoodLog):
        self.session.add(log)
        await self.session.flush()
        return log

    async def list_by_user(self, user_id, limit=50, offset=0) -> Tuple[List[MoodLog], int]:
        q = select(MoodLog).where(MoodLog.user_id == user_id).order_by(MoodLog.logged_at.desc())
        total_q = select(func.count()).select_from(MoodLog).where(MoodLog.user_id == user_id)
        total = (await self.session.execute(total_q)).scalar_one()
        res = await self.session.execute(q.limit(limit).offset(offset))
        return res.scalars().all(), total
