from __future__ import annotations

import uuid
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, Date, JSON, Index, ForeignKey, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base, IDMixin


class Squad(Base, IDMixin):
    __tablename__ = 'squads'
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_private: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))

    members: Mapped[List[SquadMember]] = relationship('SquadMember', back_populates='squad', cascade='all, delete-orphan')
    goals: Mapped[List[SquadGoal]] = relationship('SquadGoal', back_populates='squad', cascade='all, delete-orphan')


class SquadMember(Base):
    __tablename__ = 'squad_members'
    squad_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('squads.id', ondelete='CASCADE'), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role: Mapped[Optional[str]] = mapped_column(String)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    squad: Mapped[Squad] = relationship('Squad', back_populates='members')


class SquadGoal(Base, IDMixin):
    __tablename__ = 'squad_goals'
    squad_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('squads.id', ondelete='CASCADE'))
    title: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)

    squad: Mapped[Squad] = relationship('Squad', back_populates='goals')


class SquadChallenge(Base, IDMixin):
    __tablename__ = 'squad_challenges'
    squad_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('squads.id', ondelete='CASCADE'))
    title: Mapped[Optional[str]] = mapped_column(String)
    details: Mapped[Optional[str]] = mapped_column(Text)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)


class SquadChallengeProgress(Base, IDMixin):
    __tablename__ = 'squad_challenge_progress'
    challenge_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('squad_challenges.id', ondelete='CASCADE'))
    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    progress: Mapped[Optional[dict]] = mapped_column(JSON)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class Leaderboard(Base, IDMixin):
    __tablename__ = 'leaderboards'
    squad_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('squads.id', ondelete='CASCADE'))
    period: Mapped[Optional[str]] = mapped_column(String)
    standings: Mapped[Optional[dict]] = mapped_column(JSON)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

