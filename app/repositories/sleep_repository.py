from typing import List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.health import SleepLog


class SleepRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, log: SleepLog):
        self.session.add(log)
        await self.session.flush()
        return log

    async def list_by_user(self, user_id, limit=50, offset=0) -> Tuple[List[SleepLog], int]:
        q = select(SleepLog).where(SleepLog.user_id == user_id, SleepLog.is_deleted == False).order_by(SleepLog.sleep_time.desc())
        total_q = select(func.count()).select_from(SleepLog).where(SleepLog.user_id == user_id, SleepLog.is_deleted == False)
        total = (await self.session.execute(total_q)).scalar_one()
        res = await self.session.execute(q.limit(limit).offset(offset))
        return res.scalars().all(), total

    async def get(self, log_id):
        q = select(SleepLog).where(SleepLog.id == log_id, SleepLog.is_deleted == False)
        res = await self.session.execute(q)
        return res.scalars().first()
