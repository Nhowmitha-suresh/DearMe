from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task, TaskReminder, TaskComment


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: Task):
        self.session.add(task)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get(self, task_id):
        q = select(Task).where(Task.id == task_id)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def list_by_user(self, user_id) -> List[Task]:
        q = select(Task).where(Task.user_id == user_id)
        res = await self.session.execute(q)
        return res.scalars().all()

    async def add_reminder(self, reminder: TaskReminder):
        self.session.add(reminder)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(reminder)
        return reminder

    async def add_comment(self, comment: TaskComment):
        self.session.add(comment)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(comment)
        return comment
