from typing import Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: T):
        self.session = session
        self.model = model

    async def add(self, instance: T):
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def delete(self, instance: T):
        await self.session.delete(instance)
        await self.session.flush()
