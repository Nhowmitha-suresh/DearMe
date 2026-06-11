from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.repositories.water_repository import WaterRepository
from app.models.health import WaterLog
from app.schemas.health import WaterLogCreate, WaterLogRead


class WaterService:
    def __init__(self, session: AsyncSession):
        self.repo = WaterRepository(session)

    async def log_water(self, user, payload: WaterLogCreate) -> WaterLogRead:
        if payload.amount_ml <= 0:
            raise ValueError('amount_ml must be positive')
        wl = WaterLog(user_id=user.id, amount_ml=payload.amount_ml, logged_at=payload.logged_at)
        await self.repo.create(wl)
        return WaterLogRead.from_orm(wl)

    async def list_water(self, user, limit:int=50, offset:int=0):
        items, total = await self.repo.list_by_user(user.id, limit=limit, offset=offset)
        return items, total
