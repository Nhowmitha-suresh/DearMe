from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.schemas.health import WaterLogCreate, WaterLogRead
from app.core.auth import get_current_user
from app.services.water_service import WaterService
from app.services.sleep_service import SleepService
from app.schemas.health import SleepLogCreate
from app.schemas.pagination import Page
from app.services.meal_service import MealService
from app.schemas.health import MealLogCreate, WaterLogRead
from app.schemas.pagination import Page

router = APIRouter(prefix='/health', tags=['health'])


@router.post('/water', response_model=WaterLogRead)
async def log_water(payload: WaterLogCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = WaterService(db)
    try:
        return await svc.log_water(user, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/water', response_model=Page[WaterLogRead])
async def list_water(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = WaterService(db)
    items, total = await svc.list_water(user, limit=limit, offset=offset)
    return Page(items=[WaterLogRead.from_orm(i) for i in items], total=total, limit=limit, offset=offset)


@router.post('/sleep')
async def log_sleep(payload: SleepLogCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = SleepService(db)
    try:
        sl = await svc.log_sleep(user, payload)
        return {'id': str(sl.id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/sleep', response_model=Page)
async def list_sleep(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = SleepService(db)
    items, total = await svc.list_sleep(user, limit=limit, offset=offset)
    return Page(items=[{'id': str(i.id), 'sleep_time': i.sleep_time, 'wake_time': i.wake_time} for i in items], total=total, limit=limit, offset=offset)


@router.post('/meals')
async def log_meal(payload: MealLogCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = MealService(db)
    try:
        ml = await svc.log_meal(user, payload)
        return {'id': str(ml.id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/meals', response_model=Page)
async def list_meals(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = MealService(db)
    items, total = await svc.list_meals(user, limit=limit, offset=offset)
    return Page(items=[{'id': str(i.id), 'meal_type': i.meal_type, 'eaten_at': i.eaten_at, 'calories': i.calories} for i in items], total=total, limit=limit, offset=offset)


# Period cycle tracking
from datetime import date, timedelta
from app.models.health import PeriodCycle, PeriodSymptom, PeriodPrediction
from app.schemas.health import PeriodCycleCreate, PeriodCycleRead, PeriodSymptomCreate, PeriodPredictionRead

@router.post('/cycle', response_model=PeriodCycleRead, summary='Log a menstrual cycle start/end date')
async def create_cycle(payload: PeriodCycleCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    cycle = PeriodCycle(
        user_id=user.id,
        start_date=payload.start_date,
        end_date=payload.end_date
    )
    db.add(cycle)
    await db.commit()
    await db.refresh(cycle)
    return cycle


@router.get('/cycle', response_model=List[PeriodCycleRead], summary='List logged menstrual cycles')
async def list_cycles(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(PeriodCycle).where(PeriodCycle.user_id == user.id).order_by(PeriodCycle.start_date.desc())
    res = await db.execute(q)
    return res.scalars().all()


@router.post('/cycle/symptom', summary='Log a cycle symptom severity')
async def log_cycle_symptom(payload: PeriodSymptomCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    symptom = PeriodSymptom(
        cycle_id=payload.cycle_id,
        symptom=payload.symptom,
        severity=payload.severity
    )
    db.add(symptom)
    await db.commit()
    return {"message": "Symptom logged successfully"}


@router.get('/cycle/prediction', response_model=PeriodPredictionRead, summary='Predict next menstrual cycle timelines')
async def get_cycle_prediction(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    # Fetch most recent cycle to base predictions on
    q = select(PeriodCycle).where(PeriodCycle.user_id == user.id).order_by(PeriodCycle.start_date.desc()).limit(1)
    res = await db.execute(q)
    last_cycle = res.scalars().first()

    base_date = last_cycle.start_date if last_cycle else date.today()
    predicted_start = base_date + timedelta(days=28)
    predicted_end = predicted_start + timedelta(days=5)
    ovulation_date = predicted_start - timedelta(days=14)

    return PeriodPredictionRead(
        predicted_start=predicted_start,
        predicted_end=predicted_end,
        ovulation_date=ovulation_date,
        confidence=0.85
    )

