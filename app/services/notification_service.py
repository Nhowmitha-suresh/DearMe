from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, session: AsyncSession):
        self.repo = NotificationRepository(session)

    async def list_notifications(self, user, limit=50, offset=0):
        return await self.repo.list_by_user(user.id, limit=limit, offset=offset)

    async def mark_read(self, notification_id, user):
        return await self.repo.mark_read(notification_id, user.id)
