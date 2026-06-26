from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.mood_repository import MoodRepository
from app.schemas.health import WaterLogRead
from app.models.mood import MoodLog
from app.schemas.journal import JournalEntryRead
from app.schemas.health import WaterLogCreate


class MoodService:
    def __init__(self, session: AsyncSession):
        self.repo = MoodRepository(session)

    async def log_mood(self, user, mood: str, intensity: int, notes: str = None):
        if intensity < 0 or intensity > 10:
            raise ValueError('intensity must be between 0 and 10')
        ml = MoodLog(user_id=user.id, mood=mood, intensity=intensity, notes=notes)
        await self.repo.create(ml)
        return ml

    async def list_moods(self, user, limit=50, offset=0):
        return await self.repo.list_by_user(user.id, limit=limit, offset=offset)
