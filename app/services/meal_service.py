from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.meal_repository import MealRepository
from app.schemas.health import MealLogCreate
from app.models.health import MealLog


class MealService:
    def __init__(self, session: AsyncSession):
        self.repo = MealRepository(session)

    async def log_meal(self, user, payload: MealLogCreate):
        if payload.calories is not None and payload.calories < 0:
            raise ValueError('calories must be positive')
        ml = MealLog(user_id=user.id, meal_type=payload.meal_type, eaten_at=payload.eaten_at, calories=payload.calories)
        await self.repo.create(ml)
        return ml

    async def list_meals(self, user, limit=50, offset=0):
        return await self.repo.list_by_user(user.id, limit=limit, offset=offset)
