from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import date, datetime
import uuid

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.coding import CodingProfile, CodingActivity
from app.schemas.coding import (
    CodingProfileCreate,
    CodingProfileRead,
    CodingActivityCreate,
    CodingActivityRead
)

router = APIRouter(prefix='/coding', tags=['coding_hub'])


@router.post('/profile', response_model=CodingProfileRead, summary='Set or update Leetcode and Github handles')
async def upsert_coding_profile(payload: CodingProfileCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(CodingProfile).where(CodingProfile.user_id == user.id)
    res = await db.execute(q)
    profile = res.scalars().first()

    if profile:
        profile.leetcode_username = payload.leetcode_username
        profile.github_username = payload.github_username
        profile.is_active = payload.is_active if payload.is_active is not None else profile.is_active
    else:
        profile = CodingProfile(
            user_id=user.id,
            leetcode_username=payload.leetcode_username,
            github_username=payload.github_username,
            is_active=payload.is_active if payload.is_active is not None else True
        )
        db.add(profile)
        
    await db.commit()
    await db.refresh(profile)
    return profile


@router.get('/profile', response_model=CodingProfileRead, summary='Get user coding handles')
async def get_coding_profile(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(CodingProfile).where(CodingProfile.user_id == user.id)
    res = await db.execute(q)
    profile = res.scalars().first()
    if not profile:
        # Return default empty profile
        return CodingProfile(user_id=user.id, leetcode_username='', github_username='', is_active=True)
    return profile


@router.post('/activity', response_model=CodingActivityRead, summary='Log a daily coding milestone (commits, problems)')
async def log_coding_activity(payload: CodingActivityCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    logged_date = payload.logged_date or date.today()
    
    # Check if entry already exists for today to prevent duplicates
    q = select(CodingActivity).where(
        CodingActivity.user_id == user.id,
        CodingActivity.logged_date == logged_date
    )
    res = await db.execute(q)
    activity = res.scalars().first()

    if activity:
        activity.commits_count += payload.commits_count or 0
        activity.problems_solved += payload.problems_solved or 0
    else:
        activity = CodingActivity(
            user_id=user.id,
            commits_count=payload.commits_count or 0,
            problems_solved=payload.problems_solved or 0,
            logged_date=logged_date
        )
        db.add(activity)
        
    await db.commit()
    await db.refresh(activity)
    return activity


@router.get('/activity', response_model=List[CodingActivityRead], summary='List history of coding activity logs')
async def get_coding_activity_history(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(CodingActivity).where(CodingActivity.user_id == user.id).order_by(CodingActivity.logged_date.desc())
    res = await db.execute(q)
    return res.scalars().all()


@router.get('/stats', summary='Get overall aggregated coding statistics')
async def get_coding_stats(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    q = select(
        func.coalesce(func.sum(CodingActivity.commits_count), 0),
        func.coalesce(func.sum(CodingActivity.problems_solved), 0)
    ).where(CodingActivity.user_id == user.id)
    res = await db.execute(q)
    total_commits, total_problems = res.first() or (0, 0)
    
    # Calculate streak (days with problems solved or commits logged consecutively)
    streak_q = select(CodingActivity.logged_date).where(
        CodingActivity.user_id == user.id,
        (CodingActivity.commits_count > 0) | (CodingActivity.problems_solved > 0)
    ).order_by(CodingActivity.logged_date.desc())
    streak_res = await db.execute(streak_q)
    active_days = streak_res.scalars().all()
    
    streak = 0
    current_date = date.today()
    
    for d in active_days:
        diff = (current_date - d).days
        if diff == streak:
            streak += 1
        elif diff > streak:
            break
            
    return {
        "total_commits": total_commits,
        "total_problems_solved": total_problems,
        "current_streak_days": streak,
        "weekly_average_commits": round(total_commits / 4.0, 1)  # Mock average over month
    }
