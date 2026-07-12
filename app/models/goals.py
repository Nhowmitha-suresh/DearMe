from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import String, Date, DateTime, Integer, JSON, Index, ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import Enum as SAEnum

from app.models.base import Base, IDMixin, AuditMixin, GoalStatusEnum


class Goal(Base, IDMixin, AuditMixin):
    __tablename__ = 'goals'
    __table_args__ = (
        Index('ix_goals_user_id', 'user_id'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    category: Mapped[Optional[str]] = mapped_column(String)
    target_value: Mapped[Optional[float]] = mapped_column(Float)
    current_value: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[Optional[GoalStatusEnum]] = mapped_column(SAEnum(GoalStatusEnum, name='goal_status_enum'))
    goal_metadata: Mapped[Optional[dict]] = mapped_column("metadata", JSON)

    milestones: Mapped[List[GoalMilestone]] = relationship('GoalMilestone', back_populates='goal', cascade='all, delete-orphan')
    progress: Mapped[List[GoalProgress]] = relationship('GoalProgress', back_populates='goal', cascade='all, delete-orphan')


class GoalMilestone(Base, IDMixin):
    __tablename__ = 'goal_milestones'
    goal_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('goals.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String)
    target_value: Mapped[Optional[float]] = mapped_column(Float)
    due_date: Mapped[Optional[date]] = mapped_column(Date)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    goal: Mapped[Goal] = relationship('Goal', back_populates='milestones')


class GoalProgress(Base, IDMixin):
    __tablename__ = 'goal_progress'
    goal_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('goals.id', ondelete='CASCADE'), nullable=False)
    progress_value: Mapped[Optional[float]] = mapped_column(Float)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    goal: Mapped[Goal] = relationship('Goal', back_populates='progress')

