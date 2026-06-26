from typing import List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.health import WaterLog


class WaterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, log: WaterLog):
        self.session.add(log)
        await self.session.flush()
        return log

    async def get(self, log_id):
        q = select(WaterLog).where(WaterLog.id == log_id, WaterLog.is_deleted == False)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def list_by_user(self, user_id, limit=50, offset=0) -> Tuple[List[WaterLog], int]:
        q = select(WaterLog).where(WaterLog.user_id == user_id, WaterLog.is_deleted == False).order_by(WaterLog.logged_at.desc())
        total_q = select(func.count()).select_from(WaterLog).where(WaterLog.user_id == user_id, WaterLog.is_deleted == False)
        total = (await self.session.execute(total_q)).scalar_one()
        res = await self.session.execute(q.limit(limit).offset(offset))
        return res.scalars().all(), total
