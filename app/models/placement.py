from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, Integer, JSON, ForeignKey, Float, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base, IDMixin


class Company(Base, IDMixin):
    __tablename__ = 'companies'
    name: Mapped[str] = mapped_column(String, nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String)
    industry: Mapped[Optional[str]] = mapped_column(String)

    roles: Mapped[List[JobRole]] = relationship('JobRole', back_populates='company', cascade='all, delete-orphan')


class JobRole(Base, IDMixin):
    __tablename__ = 'job_roles'
    company_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('companies.id', ondelete='CASCADE'))
    title: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String)
    level: Mapped[Optional[str]] = mapped_column(String)

    company: Mapped[Company] = relationship('Company', back_populates='roles')


class Application(Base, IDMixin):
    __tablename__ = 'applications'
    __table_args__ = (
        Index('ix_applications_user_id', 'user_id'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('companies.id'))
    role_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('job_roles.id'))
    status: Mapped[Optional[str]] = mapped_column(String)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    app_metadata: Mapped[Optional[dict]] = mapped_column("metadata", JSON)


    company: Mapped[Optional[Company]] = relationship('Company')
    role: Mapped[Optional[JobRole]] = relationship('JobRole')
    assessments: Mapped[List[Assessment]] = relationship('Assessment', back_populates='application', cascade='all, delete-orphan')
    interviews: Mapped[List[Interview]] = relationship('Interview', back_populates='application', cascade='all, delete-orphan')


class Assessment(Base, IDMixin):
    __tablename__ = 'assessments'
    application_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('applications.id', ondelete='CASCADE'))
    assessment_type: Mapped[Optional[str]] = mapped_column(String)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)

    application: Mapped[Application] = relationship('Application', back_populates='assessments')
    scores: Mapped[List[AssessmentScore]] = relationship('AssessmentScore', back_populates='assessment', cascade='all, delete-orphan')


class AssessmentScore(Base, IDMixin):
    __tablename__ = 'assessment_scores'
    assessment_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('assessments.id', ondelete='CASCADE'))
    score: Mapped[Optional[float]] = mapped_column(Float)
    details: Mapped[Optional[dict]] = mapped_column(JSON)

    assessment: Mapped[Assessment] = relationship('Assessment', back_populates='scores')


class Interview(Base, IDMixin):
    __tablename__ = 'interviews'
    application_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('applications.id', ondelete='CASCADE'))
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    interviewer: Mapped[Optional[str]] = mapped_column(String)
    location: Mapped[Optional[str]] = mapped_column(String)
    result: Mapped[Optional[str]] = mapped_column(String)

    application: Mapped[Application] = relationship('Application', back_populates='interviews')
    feedbacks: Mapped[List[InterviewFeedback]] = relationship('InterviewFeedback', back_populates='interview', cascade='all, delete-orphan')


class InterviewFeedback(Base, IDMixin):
    __tablename__ = 'interview_feedback'
    interview_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('interviews.id', ondelete='CASCADE'))
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    rating: Mapped[Optional[int]] = mapped_column(Integer)

    interview: Mapped[Interview] = relationship('Interview', back_populates='feedbacks')

