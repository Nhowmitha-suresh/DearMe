from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.health import WaterLogCreate, WaterLogRead, SleepLogCreate, MealLogCreate
from app.models.health import WaterLog, SleepLog, MealLog
from app.core.auth import get_current_user

router = APIRouter(prefix='/health', tags=['health'])


@router.post('/water', response_model=WaterLogRead)
async def log_water(payload: WaterLogCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    wl = WaterLog(user_id=user.id, amount_ml=payload.amount_ml, logged_at=payload.logged_at)
    db.add(wl)
    await db.flush()
    return WaterLogRead.from_orm(wl)


@router.get('/water', response_model=List[WaterLogRead])
async def list_water(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    q = await db.execute('SELECT * FROM water_logs WHERE user_id = :uid AND is_deleted = false ORDER BY logged_at DESC LIMIT 100', {'uid': str(user.id)})
    return []
