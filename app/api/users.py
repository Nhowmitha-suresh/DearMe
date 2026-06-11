from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserRead)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    svc = UserService(db)
    user = await svc.create_user(payload)
    return user


@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    svc = UserService(db)
    user = await svc.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return UserRead.from_orm(user)


@router.get('/', response_model=List[UserRead])
async def list_users(limit: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    # simple listing via direct query (could move to repo)
    q = await db.execute('SELECT * FROM users WHERE is_deleted = false LIMIT :lim', {'lim': limit})
    rows = q.fetchall()
    return []
