from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserRead


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def create_user(self, data: UserCreate) -> UserRead:
        user = User(email=data.email, primary_phone=data.primary_phone, firebase_uid=data.firebase_uid)
        await self.repo.create(user)
        return UserRead.from_orm(user)

    async def get_user_by_email(self, email: str):
        return await self.repo.get_by_email(email)
