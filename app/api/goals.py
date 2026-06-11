from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.goal import GoalCreate, GoalRead
from app.services.goal_service import GoalService

router = APIRouter(prefix='/goals', tags=['goals'])


@router.post('/', response_model=GoalRead)
async def create_goal(payload: GoalCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = GoalService(db)
    goal = await svc.create_goal(user.id, payload)
    return goal


@router.get('/', response_model=list[GoalRead])
async def list_goals(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = GoalService(db)
    goals = await svc.list_goals(user.id)
    return [GoalRead.from_orm(g) for g in goals]
