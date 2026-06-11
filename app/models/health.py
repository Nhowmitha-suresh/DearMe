from __future__ import annotations

import uuid
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import Integer, String, Date, DateTime, Text, JSON, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import Enum as SAEnum

from app.models.base import Base, IDMixin, AuditMixin, SoftDeleteMixin, MealTypeEnum, PeriodFlowEnum


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
        Index('ix_water_logs_log_date', 'logged_at')
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
    __table_args__ = (
        Index('ix_sleep_logs_user_id', 'user_id'),
    )

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
    __table_args__ = (
        Index('ix_meal_logs_user_id', 'user_id'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    meal_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('meals.id'), nullable=True)
    meal_type: Mapped[Optional[str]] = mapped_column(SAEnum(MealTypeEnum, name='meal_type_enum'))
    eaten_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    calories: Mapped[Optional[int]] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    meal = relationship('Meal')
    images: Mapped[List['MealImage']] = relationship('MealImage', back_populates='meal_log', cascade='all, delete-orphan')


class MealImage(Base, IDMixin):
    __tablename__ = 'meal_images'
    meal_log_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('meal_logs.id', ondelete='CASCADE'), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    meal_log = relationship('MealLog', back_populates='images')


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
import sqlalchemy as sa
from sqlalchemy import Column, Integer, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin, SoftDeleteMixin

meal_type_enum = ENUM('breakfast','lunch','dinner','snack', name='meal_type_enum', create_type=False)


class WaterGoal(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'water_goals'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    daily_goal_ml = Column(Integer, default=2000, nullable=False)
    effective_date = Column(sa.Date, default=sa.func.current_date())


class WaterLog(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'water_logs'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    amount_ml = Column(Integer, nullable=False)
    logged_at = Column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    notes = Column(Text)


class SleepScore(Base, IDMixin, TimestampMixin):
    __tablename__ = 'sleep_scores'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    score = Column(Integer)
    calculated_at = Column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    details = Column(JSON)


class SleepLog(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'sleep_logs'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    sleep_time = Column(sa.TIMESTAMP(timezone=True))
    wake_time = Column(sa.TIMESTAMP(timezone=True))
    duration_minutes = Column(Integer)
    quality = Column(Integer)
    notes = Column(Text)


class Meal(Base, IDMixin, TimestampMixin):
    __tablename__ = 'meals'
    name = Column(Text)
    meal_type = Column(meal_type_enum)
    default_calories = Column(Integer)


class MealLog(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'meal_logs'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    meal_id = Column(UUID(as_uuid=True), sa.ForeignKey('meals.id'))
    meal_type = Column(meal_type_enum)
    eaten_at = Column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    calories = Column(Integer)
    notes = Column(Text)

    meal = relationship('Meal')


class MealImage(Base, IDMixin, TimestampMixin):
    __tablename__ = 'meal_images'
    meal_log_id = Column(UUID(as_uuid=True), sa.ForeignKey('meal_logs.id', ondelete='CASCADE'), nullable=False)
    url = Column(Text)
    metadata = Column(JSON)


class PeriodCycle(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'period_cycles'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    start_date = Column(sa.Date, nullable=False)
    end_date = Column(sa.Date)
    flow = Column(ENUM('light','medium','heavy','spotting','none', name='period_flow_enum', create_type=False))
    pain_level = Column(Integer)
    notes = Column(Text)


class PeriodSymptom(Base, IDMixin, TimestampMixin):
    __tablename__ = 'period_symptoms'
    cycle_id = Column(UUID(as_uuid=True), sa.ForeignKey('period_cycles.id', ondelete='CASCADE'), nullable=False)
    symptom = Column(Text)
    severity = Column(Integer)
    recorded_at = Column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())


class PeriodPrediction(Base, IDMixin, TimestampMixin):
    __tablename__ = 'period_predictions'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    predicted_start = Column(sa.Date)
    predicted_end = Column(sa.Date)
    ovulation_date = Column(sa.Date)
    pms_window = Column(JSON)
    confidence = Column(sa.Numeric(5,4))
