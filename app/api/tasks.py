from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.task import TaskCreate, TaskRead
from app.services.task_service import TaskService

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('/', response_model=TaskRead)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = TaskService(db)
    task = await svc.create_task(user.id, payload)
    return task


@router.get('/', response_model=list[TaskRead])
async def list_tasks(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = TaskService(db)
    tasks = await svc.list_tasks(user.id)
    return [TaskRead.from_orm(t) for t in tasks]
