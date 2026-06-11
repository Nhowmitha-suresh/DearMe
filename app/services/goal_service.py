from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.goal_repository import GoalRepository
from app.schemas.goal import GoalCreate, GoalRead
from app.models.goals import Goal


class GoalService:
    def __init__(self, session: AsyncSession):
        self.repo = GoalRepository(session)

    async def create_goal(self, user_id, data: GoalCreate) -> GoalRead:
        goal = Goal(user_id=user_id, title=data.title, description=data.description, category=data.category)
        await self.repo.create(goal)
        return GoalRead.from_orm(goal)

    async def list_goals(self, user_id):
        return await self.repo.list_by_user(user_id)
