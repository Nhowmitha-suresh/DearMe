from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user
from app.services.life_service import LifeScoreService
from app.schemas.pagination import Page

router = APIRouter(prefix='/analytics', tags=['analytics'])


@router.post('/life_scores', response_model=dict)
async def calculate_life_score(components: dict, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = LifeScoreService(db)
    ls = await svc.calculate_and_store(user, components)
    return {'id': str(ls.id), 'score': ls.score, 'calculated_at': ls.calculated_at}


@router.get('/life_scores', response_model=Page)
async def list_life_scores(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = LifeScoreService(db)
    items, total = await svc.list_scores(user, limit=limit, offset=offset)
    return Page(items=[{'id': str(i.id), 'score': i.score, 'calculated_at': i.calculated_at, 'components': i.components} for i in items], total=total, limit=limit, offset=offset)
