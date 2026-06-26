from typing import List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.health import PeriodCycle, PeriodPrediction


class PeriodRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_cycle(self, cycle: PeriodCycle):
        self.session.add(cycle)
        await self.session.flush()
        return cycle

    async def list_cycles(self, user_id, limit=50, offset=0) -> Tuple[List[PeriodCycle], int]:
        q = select(PeriodCycle).where(PeriodCycle.user_id == user_id, PeriodCycle.is_deleted == False).order_by(PeriodCycle.start_date.desc())
        total_q = select(func.count()).select_from(PeriodCycle).where(PeriodCycle.user_id == user_id, PeriodCycle.is_deleted == False)
        total = (await self.session.execute(total_q)).scalar_one()
        res = await self.session.execute(q.limit(limit).offset(offset))
        return res.scalars().all(), total

    async def add_prediction(self, pred: PeriodPrediction):
        self.session.add(pred)
        await self.session.flush()
        return pred
