from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goals import Goal, GoalMilestone, GoalProgress


class GoalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, goal: Goal):
        self.session.add(goal)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def get(self, goal_id):
        q = select(Goal).where(Goal.id == goal_id)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def list_by_user(self, user_id) -> List[Goal]:
        q = select(Goal).where(Goal.user_id == user_id)
        res = await self.session.execute(q)
        return res.scalars().all()

    async def add_milestone(self, milestone: GoalMilestone):
        self.session.add(milestone)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(milestone)
        return milestone

    async def add_progress(self, progress: GoalProgress):
        self.session.add(progress)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(progress)
        return progress
