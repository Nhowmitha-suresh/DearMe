from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.user import UserCreate, UserRead, UserProfileCreate
from app.services.user_service import UserService
from app.models.user import UserProfile, UserSetting

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserRead)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    svc = UserService(db)
    user = await svc.create_user(payload)
    return user


@router.post('/profile', summary='Create or update user profile and placement settings')
async def update_profile(payload: UserProfileCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    profile_query = select(UserProfile).where(UserProfile.user_id == user.id)
    profile_res = await db.execute(profile_query)
    profile = profile_res.scalars().first()
    
    if not profile:
        profile = UserProfile(user_id=user.id)
        db.add(profile)
        
    profile.first_name = payload.first_name
    profile.last_name = payload.last_name
    profile.college = payload.college
    profile.department = payload.department
    profile.year = payload.year
    profile.student_roll_no = payload.student_roll_no
    
    setting_query = select(UserSetting).where(UserSetting.user_id == user.id, UserSetting.key == 'placement_profile')
    setting_res = await db.execute(setting_query)
    setting = setting_res.scalars().first()
    
    placement_data = {
        "gpa": payload.gpa,
        "skills": payload.skills,
        "target_roles": payload.target_roles
    }
    
    if not setting:
        setting = UserSetting(user_id=user.id, key='placement_profile', value=placement_data)
        db.add(setting)
    else:
        setting.value = placement_data
        
    await db.commit()
    return {"message": "Profile and placement customizations saved successfully"}


@router.get('/profile/me', summary='Get current authenticated user profile and placement details')
async def get_my_profile(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    profile_query = select(UserProfile).where(UserProfile.user_id == user.id)
    profile_res = await db.execute(profile_query)
    profile = profile_res.scalars().first()
    
    setting_query = select(UserSetting).where(UserSetting.user_id == user.id, UserSetting.key == 'placement_profile')
    setting_res = await db.execute(setting_query)
    setting = setting_res.scalars().first()
    
    gpa = None
    skills = []
    target_roles = []
    if setting and setting.value:
        gpa = setting.value.get("gpa")
        skills = setting.value.get("skills", [])
        target_roles = setting.value.get("target_roles", [])
        
    return {
        "first_name": profile.first_name if profile else None,
        "last_name": profile.last_name if profile else None,
        "college": profile.college if profile else None,
        "department": profile.department if profile else None,
        "year": profile.year if profile else None,
        "student_roll_no": profile.student_roll_no if profile else None,
        "gpa": gpa,
        "skills": skills,
        "target_roles": target_roles
    }


@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    svc = UserService(db)
    user = await svc.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return UserRead.from_orm(user)


@router.get('/', response_model=List[UserRead])
async def list_users(limit: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    svc = UserService(db)
    users = await svc.list_users(limit=limit)
    return [UserRead.from_orm(user) for user in users]
