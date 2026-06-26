from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.period_repository import PeriodRepository
from app.models.health import PeriodCycle, PeriodPrediction


class PeriodService:
    def __init__(self, session: AsyncSession):
        self.repo = PeriodRepository(session)

    async def create_cycle(self, user, start_date, end_date=None, flow=None, pain_level=None, notes=None):
        cycle = PeriodCycle(user_id=user.id, start_date=start_date, end_date=end_date, flow=flow, pain_level=pain_level, notes=notes)
        await self.repo.create_cycle(cycle)
        return cycle

    async def list_cycles(self, user, limit=50, offset=0):
        return await self.repo.list_cycles(user.id, limit=limit, offset=offset)

    async def add_prediction(self, user, predicted_start, predicted_end, ovulation_date=None, pms_window=None, confidence=None):
        pred = PeriodPrediction(user_id=user.id, predicted_start=predicted_start, predicted_end=predicted_end, ovulation_date=ovulation_date, pms_window=pms_window, confidence=confidence)
        await self.repo.add_prediction(pred)
        return pred
