from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import String, Date, Integer, JSON, Index, ForeignKey
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
    target_value: Mapped[Optional[float]] = mapped_column(JSON)
    current_value: Mapped[Optional[float]] = mapped_column(JSON, default=0)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[Optional[str]] = mapped_column(SAEnum(GoalStatusEnum, name='goal_status_enum'))
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    milestones: Mapped[List['GoalMilestone']] = relationship('GoalMilestone', back_populates='goal', cascade='all, delete-orphan')
    progress: Mapped[List['GoalProgress']] = relationship('GoalProgress', back_populates='goal', cascade='all, delete-orphan')


class GoalMilestone(Base, IDMixin):
    __tablename__ = 'goal_milestones'
    goal_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('goals.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String)
    target_value: Mapped[Optional[float]] = mapped_column(JSON)
    due_date: Mapped[Optional[date]] = mapped_column(Date)
    completed: Mapped[bool] = mapped_column(Integer, default=0)

    goal = relationship('Goal', back_populates='milestones')


class GoalProgress(Base, IDMixin):
    __tablename__ = 'goal_progress'
    goal_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('goals.id', ondelete='CASCADE'), nullable=False)
    progress_value: Mapped[Optional[float]] = mapped_column(JSON)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    goal = relationship('Goal', back_populates='progress')
import sqlalchemy as sa
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin

goal_status = ENUM('not_started','in_progress','paused','completed','abandoned', name='goal_status_enum', create_type=False)


class Goal(Base, IDMixin, TimestampMixin):
    __tablename__ = 'goals'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    category = Column(Text)
    target_value = Column(sa.Numeric)
    current_value = Column(sa.Numeric, default=0)
    status = Column(goal_status, server_default='not_started')

    milestones = relationship('GoalMilestone', back_populates='goal', cascade='all, delete-orphan')


class GoalMilestone(Base, IDMixin, TimestampMixin):
    __tablename__ = 'goal_milestones'
    goal_id = Column(UUID(as_uuid=True), sa.ForeignKey('goals.id', ondelete='CASCADE'), nullable=False)
    title = Column(Text)
    target_value = Column(sa.Numeric)
    due_date = Column(sa.Date)
    completed = Column(sa.Boolean, default=False)

    goal = relationship('Goal', back_populates='milestones')


class GoalProgress(Base, IDMixin, TimestampMixin):
    __tablename__ = 'goal_progress'
    goal_id = Column(UUID(as_uuid=True), sa.ForeignKey('goals.id', ondelete='CASCADE'), nullable=False)
    progress_value = Column(sa.Numeric)
    recorded_at = Column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
