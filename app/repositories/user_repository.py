from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserPreference, UserProfile


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id):
        q = select(User).where(User.id == user_id, User.is_deleted == False)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        q = select(User).where(User.email == email, User.is_deleted == False)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def list(self, limit: int = 20, offset: int = 0):
        q = select(User).where(User.is_deleted == False).offset(offset).limit(limit)
        res = await self.session.execute(q)
        return res.scalars().all()

    async def create(self, user: User):
        self.session.add(user)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User):
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def add_profile(self, profile: UserProfile):
        self.session.add(profile)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def set_preferences(self, pref: UserPreference):
        self.session.add(pref)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(pref)
        return pref
