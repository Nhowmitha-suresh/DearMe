from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime
import uuid

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.placement import Company, JobRole, Application, Interview
from app.schemas.career import (
    CompanyCreate,
    CompanyRead,
    JobRoleCreate,
    JobRoleRead,
    ApplicationCreate,
    ApplicationRead
)

router = APIRouter(prefix='/career', tags=['career_hub'])


@router.post('/companies', response_model=CompanyRead, summary='Register a company profile')
async def create_company(payload: CompanyCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    company = Company(
        name=payload.name,
        website=payload.website,
        industry=payload.industry
    )
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company


@router.get('/companies', response_model=List[CompanyRead], summary='List registered companies')
async def get_companies(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(Company).order_by(Company.name.asc())
    res = await db.execute(q)
    return res.scalars().all()


@router.post('/roles', response_model=JobRoleRead, summary='Create a job role listing')
async def create_job_role(payload: JobRoleCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    role = JobRole(
        company_id=payload.company_id,
        title=payload.title,
        description=payload.description,
        location=payload.location,
        level=payload.level
    )
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


@router.get('/roles', response_model=List[JobRoleRead], summary='List available job roles')
async def get_job_roles(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(JobRole)
    res = await db.execute(q)
    return res.scalars().all()


@router.post('/applications', response_model=ApplicationRead, summary='Log a job application submission')
async def create_application(payload: ApplicationCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    app = Application(
        user_id=user.id,
        company_id=payload.company_id,
        role_id=payload.role_id,
        status=payload.status or 'applied',
        applied_at=payload.applied_at or datetime.utcnow(),
        app_metadata=payload.app_metadata or {}
    )
    db.add(app)
    await db.commit()
    await db.refresh(app)
    return app


@router.get('/applications', response_model=List[ApplicationRead], summary='Get history of logged job applications')
async def get_applications(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(Application).where(Application.user_id == user.id).order_by(Application.applied_at.desc())
    res = await db.execute(q)
    return res.scalars().all()


@router.put('/applications/{app_id}', response_model=ApplicationRead, summary='Update job application status pipeline')
async def update_application_status(app_id: uuid.UUID, status_str: str, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(Application).where(
        Application.id == app_id,
        Application.user_id == user.id
    )
    res = await db.execute(q)
    app = res.scalars().first()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Application not found')
        
    app.status = status_str
    await db.commit()
    await db.refresh(app)
    return app


@router.get('/stats', summary='Get placement progress metrics')
async def get_placement_stats(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    # Total apps count
    apps_q = select(func.count(Application.id)).where(Application.user_id == user.id)
    apps_res = await db.execute(apps_q)
    total_apps = apps_res.scalar_one()

    # Interview count
    interview_q = select(func.count(Interview.id)).join(
        Application, Application.id == Interview.application_id
    ).where(Application.user_id == user.id)
    interview_res = await db.execute(interview_q)
    total_interviews = interview_res.scalar_one()

    # Offers count
    offers_q = select(func.count(Application.id)).where(
        Application.user_id == user.id,
        Application.status == 'offered'
    )
    offers_res = await db.execute(offers_q)
    total_offers = offers_res.scalar_one()

    return {
        "total_applications": total_apps,
        "total_interviews": total_interviews,
        "total_offers": total_offers,
        "interview_ratio": round(total_interviews / total_apps, 2) if total_apps > 0 else 0.0
    }
