from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple
from app.repositories.sleep_repository import SleepRepository
from app.models.health import SleepLog
from app.schemas.health import SleepLogCreate
from app.schemas.health import WaterLogRead


class SleepService:
    def __init__(self, session: AsyncSession):
        self.repo = SleepRepository(session)

    async def log_sleep(self, user, payload: SleepLogCreate):
        if payload.wake_time <= payload.sleep_time:
            raise ValueError('wake_time must be after sleep_time')
        sl = SleepLog(user_id=user.id, sleep_time=payload.sleep_time, wake_time=payload.wake_time,
                      duration_minutes=int((payload.wake_time - payload.sleep_time).total_seconds() / 60))
        await self.repo.create(sl)
        return sl

    async def list_sleep(self, user, limit=50, offset=0) -> Tuple[List[SleepLog], int]:
        return await self.repo.list_by_user(user.id, limit=limit, offset=offset)
