from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskRead
from app.models.tasks import Task


class TaskService:
    def __init__(self, session: AsyncSession):
        self.repo = TaskRepository(session)

    async def create_task(self, user_id, data: TaskCreate) -> TaskRead:
        task = Task(user_id=user_id, title=data.title, description=data.description)
        await self.repo.create(task)
        return TaskRead.from_orm(task)

    async def list_tasks(self, user_id):
        return await self.repo.list_by_user(user_id)
