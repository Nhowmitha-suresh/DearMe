import uuid
from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base, IDMixin, AuditMixin, SoftDeleteMixin


class Expense(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'expenses'

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class SavingsGoal(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'savings_goals'

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    target_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    current_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)
    target_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
