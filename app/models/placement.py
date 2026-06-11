from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base, IDMixin


class Company(Base, IDMixin):
    __tablename__ = 'companies'
    name: Mapped[str] = mapped_column(String, nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String)
    industry: Mapped[Optional[str]] = mapped_column(String)


class JobRole(Base, IDMixin):
    __tablename__ = 'job_roles'
    company_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('companies.id', ondelete='CASCADE'))
    title: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String)
    level: Mapped[Optional[str]] = mapped_column(String)


class Application(Base, IDMixin):
    __tablename__ = 'applications'
    __table_args__ = (
        Index('ix_applications_user_id', 'user_id'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('companies.id'))
    role_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('job_roles.id'))
    status: Mapped[Optional[str]] = mapped_column(String)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)


class Assessment(Base, IDMixin):
    __tablename__ = 'assessments'
    application_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('applications.id', ondelete='CASCADE'))
    assessment_type: Mapped[Optional[str]] = mapped_column(String)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)


class AssessmentScore(Base, IDMixin):
    __tablename__ = 'assessment_scores'
    assessment_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('assessments.id', ondelete='CASCADE'))
    score: Mapped[Optional[float]] = mapped_column(JSON)
    details: Mapped[Optional[dict]] = mapped_column(JSON)


class Interview(Base, IDMixin):
    __tablename__ = 'interviews'
    application_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('applications.id', ondelete='CASCADE'))
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    interviewer: Mapped[Optional[str]] = mapped_column(String)
    location: Mapped[Optional[str]] = mapped_column(String)
    result: Mapped[Optional[str]] = mapped_column(String)


class InterviewFeedback(Base, IDMixin):
    __tablename__ = 'interview_feedback'
    interview_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('interviews.id', ondelete='CASCADE'))
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
import sqlalchemy as sa
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin


class Company(Base, IDMixin, TimestampMixin):
    __tablename__ = 'companies'
    name = Column(Text, nullable=False)
    website = Column(Text)
    industry = Column(Text)

    roles = relationship('JobRole', back_populates='company', cascade='all, delete-orphan')


class JobRole(Base, IDMixin, TimestampMixin):
    __tablename__ = 'job_roles'
    company_id = Column(UUID(as_uuid=True), sa.ForeignKey('companies.id', ondelete='CASCADE'))
    title = Column(Text)
    description = Column(Text)
    location = Column(Text)
    level = Column(Text)

    company = relationship('Company', back_populates='roles')


class Application(Base, IDMixin, TimestampMixin):
    __tablename__ = 'applications'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), sa.ForeignKey('companies.id'))
    role_id = Column(UUID(as_uuid=True), sa.ForeignKey('job_roles.id'))
    status = Column(Text)
    applied_at = Column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    metadata = Column(sa.JSON)


class Assessment(Base, IDMixin, TimestampMixin):
    __tablename__ = 'assessments'
    application_id = Column(UUID(as_uuid=True), sa.ForeignKey('applications.id', ondelete='CASCADE'))
    assessment_type = Column(Text)
    scheduled_at = Column(sa.TIMESTAMP(timezone=True))
    duration_minutes = Column(sa.Integer)


class AssessmentScore(Base, IDMixin):
    __tablename__ = 'assessment_scores'
    assessment_id = Column(UUID(as_uuid=True), sa.ForeignKey('assessments.id', ondelete='CASCADE'))
    score = Column(sa.Numeric)
    details = Column(sa.JSON)


class Interview(Base, IDMixin, TimestampMixin):
    __tablename__ = 'interviews'
    application_id = Column(UUID(as_uuid=True), sa.ForeignKey('applications.id', ondelete='CASCADE'))
    scheduled_at = Column(sa.TIMESTAMP(timezone=True))
    interviewer = Column(Text)
    location = Column(Text)
    result = Column(Text)


class InterviewFeedback(Base, IDMixin, TimestampMixin):
    __tablename__ = 'interview_feedback'
    interview_id = Column(UUID(as_uuid=True), sa.ForeignKey('interviews.id', ondelete='CASCADE'))
    feedback = Column(Text)
    rating = Column(sa.Integer)
