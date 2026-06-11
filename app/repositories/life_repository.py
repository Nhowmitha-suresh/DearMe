from typing import Tuple, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.analytics import LifeScore


class LifeScoreRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def create(self, life_score: LifeScore):
		self.session.add(life_score)
		await self.session.flush()
		return life_score

	async def list_by_user(self, user_id, limit=50, offset=0) -> Tuple[List[LifeScore], int]:
		q = select(LifeScore).where(LifeScore.user_id == user_id).order_by(LifeScore.calculated_at.desc())
		total_q = select(func.count()).select_from(LifeScore).where(LifeScore.user_id == user_id)
		total = (await self.session.execute(total_q)).scalar_one()
		res = await self.session.execute(q.limit(limit).offset(offset))
		return res.scalars().all(), total

