from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.journal_repository import JournalRepository
from app.models.journal import JournalEntry
from app.schemas.journal import JournalEntryCreate


class JournalService:
    def __init__(self, session: AsyncSession):
        self.repo = JournalRepository(session)

    async def create_entry(self, user, payload: JournalEntryCreate):
        if not payload.content or payload.content.strip() == '':
            raise ValueError('content is required')
        je = JournalEntry(user_id=user.id, title=payload.title, content=payload.content, mood=payload.mood)
        await self.repo.create(je)
        return je

    async def list_entries(self, user, limit=50, offset=0):
        return await self.repo.list_by_user(user.id, limit=limit, offset=offset)
