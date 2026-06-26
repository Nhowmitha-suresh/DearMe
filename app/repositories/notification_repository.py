from typing import List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notifications import Notification


class NotificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_by_user(self, user_id, limit=50, offset=0) -> Tuple[List[Notification], int]:
        q = select(Notification).where(Notification.user_id == user_id).order_by(Notification.scheduled_at.desc())
        total_q = select(func.count()).select_from(Notification).where(Notification.user_id == user_id)
        total = (await self.session.execute(total_q)).scalar_one()
        res = await self.session.execute(q.limit(limit).offset(offset))
        return res.scalars().all(), total

    async def mark_read(self, notification_id, user_id):
        q = select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
        res = await self.session.execute(q)
        n = res.scalars().first()
        if not n:
            return None
        n.read_at = func.now()
        await self.session.flush()
        return n
