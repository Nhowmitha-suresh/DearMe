from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserProfile, UserPreference


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

    async def create(self, user: User):
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(self, user: User):
        await self.session.flush()
        return user

    async def add_profile(self, profile: UserProfile):
        self.session.add(profile)
        await self.session.flush()
        return profile

    async def set_preferences(self, pref: UserPreference):
        self.session.add(pref)
        await self.session.flush()
        return pref
