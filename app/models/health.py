from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, Base, IDMixin, MealTypeEnum, PeriodFlowEnum, SoftDeleteMixin


class WaterGoal(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'water_goals'
    __table_args__ = (Index('ix_water_goals_user_id', 'user_id'),)

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    daily_goal_ml: Mapped[int] = mapped_column(Integer, nullable=False, default=2000)
    effective_date: Mapped[date] = mapped_column(Date, default=date.today)


class WaterLog(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'water_logs'
    __table_args__ = (
        Index('ix_water_logs_user_id', 'user_id'),
        Index('ix_water_logs_log_date', 'logged_at'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    amount_ml: Mapped[int] = mapped_column(Integer, nullable=False)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class SleepScore(Base, IDMixin):
    __tablename__ = 'sleep_scores'

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    score: Mapped[Optional[int]] = mapped_column(Integer)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    details: Mapped[Optional[dict]] = mapped_column(JSON)


class SleepLog(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'sleep_logs'
    __table_args__ = (Index('ix_sleep_logs_user_id', 'user_id'),)

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    sleep_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    wake_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    quality: Mapped[Optional[int]] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class Meal(Base, IDMixin):
    __tablename__ = 'meals'

    name: Mapped[Optional[str]] = mapped_column(String)
    meal_type: Mapped[Optional[str]] = mapped_column(SAEnum(MealTypeEnum, name='meal_type_enum'))
    default_calories: Mapped[Optional[int]] = mapped_column(Integer)


class MealLog(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'meal_logs'
    __table_args__ = (Index('ix_meal_logs_user_id', 'user_id'),)

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    meal_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('meals.id'), nullable=True)
    meal_type: Mapped[Optional[str]] = mapped_column(SAEnum(MealTypeEnum, name='meal_type_enum'))
    eaten_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    calories: Mapped[Optional[int]] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    meal: Mapped[Optional['Meal']] = relationship('Meal')
    images: Mapped[List['MealImage']] = relationship('MealImage', back_populates='meal_log', cascade='all, delete-orphan')


class MealImage(Base, IDMixin):
    __tablename__ = 'meal_images'

    meal_log_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('meal_logs.id', ondelete='CASCADE'), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String)
    image_metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    meal_log: Mapped['MealLog'] = relationship('MealLog', back_populates='images')


class PeriodCycle(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'period_cycles'

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    flow: Mapped[Optional[str]] = mapped_column(SAEnum(PeriodFlowEnum, name='period_flow_enum'))
    pain_level: Mapped[Optional[int]] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class PeriodSymptom(Base, IDMixin):
    __tablename__ = 'period_symptoms'

    cycle_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('period_cycles.id', ondelete='CASCADE'), nullable=False)
    symptom: Mapped[Optional[str]] = mapped_column(String)
    severity: Mapped[Optional[int]] = mapped_column(Integer)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class PeriodPrediction(Base, IDMixin):
    __tablename__ = 'period_predictions'

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    predicted_start: Mapped[Optional[date]] = mapped_column(Date)
    predicted_end: Mapped[Optional[date]] = mapped_column(Date)
    ovulation_date: Mapped[Optional[date]] = mapped_column(Date)
    pms_window: Mapped[Optional[dict]] = mapped_column(JSON)
    confidence: Mapped[Optional[float]] = mapped_column(Integer)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
