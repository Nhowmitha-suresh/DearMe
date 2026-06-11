from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.life_repository import LifeScoreRepository
from app.models.analytics import LifeScore
from datetime import datetime


class LifeScoreService:
    def __init__(self, session: AsyncSession):
        self.repo = LifeScoreRepository(session)

    async def calculate_and_store(self, user, components: dict):
        # Simple aggregation example — production should use real analytics
        score = float(sum(v for v in components.values())) / max(1, len(components))
        ls = LifeScore(user_id=user.id, score=score, components=components, calculated_at=datetime.utcnow())
        await self.repo.create(ls)
        return ls

    async def list_scores(self, user, limit=50, offset=0):
        return await self.repo.list_by_user(user.id, limit=limit, offset=offset)
