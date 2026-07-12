from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional
from sqlalchemy import JSON, DateTime, ForeignKey, Index, Float, Integer, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base, IDMixin


class DailyMetric(Base, IDMixin):
    __tablename__ = 'daily_metrics'
    __table_args__ = (
        UniqueConstraint('user_id', 'metric_date', name='uq_daily_metric_user_date'),
        Index('idx_daily_metrics_user_date', 'user_id', 'metric_date'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    metric_date: Mapped[date] = mapped_column(Date, nullable=False)
    sleep_score: Mapped[Optional[float]] = mapped_column(Float)
    water_ml: Mapped[Optional[int]] = mapped_column(Integer)
    mood_score: Mapped[Optional[float]] = mapped_column(Float)
    study_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    coding_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    task_completion_rate: Mapped[Optional[float]] = mapped_column(Float)
    habit_completion_rate: Mapped[Optional[float]] = mapped_column(Float)
    journal_entries_count: Mapped[int] = mapped_column(Integer, default=0)
    sleep_duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    life_score: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class WeeklyMetric(Base, IDMixin):
    __tablename__ = 'weekly_metrics'
    __table_args__ = (
        UniqueConstraint('user_id', 'week_start', name='uq_weekly_metric_user_week'),
        Index('idx_weekly_metrics_user_week', 'user_id', 'week_start'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    week_start: Mapped[date] = mapped_column(Date, nullable=False)
    metrics: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class MonthlyMetric(Base, IDMixin):
    __tablename__ = 'monthly_metrics'
    __table_args__ = (
        UniqueConstraint('user_id', 'month_start', name='uq_monthly_metric_user_month'),
        Index('idx_monthly_metrics_user_month', 'user_id', 'month_start'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    month_start: Mapped[date] = mapped_column(Date, nullable=False)
    metrics: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class LifeScore(Base, IDMixin):
    __tablename__ = 'life_scores'

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    score: Mapped[Optional[float]] = mapped_column(Float)
    components: Mapped[Optional[dict]] = mapped_column(JSON)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

