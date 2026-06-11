from __future__ import annotations

from typing import List, Optional
import uuid
from sqlalchemy import String, Integer, JSON, Index, Date, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base, IDMixin, AuditMixin, SoftDeleteMixin, GenderEnum


class User(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'users'
    __table_args__ = (
        Index('ix_users_email', 'email'),
    )

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    primary_phone: Mapped[Optional[str]] = mapped_column(String)
    firebase_uid: Mapped[Optional[str]] = mapped_column(String, unique=True)

    profiles: Mapped[List['UserProfile']] = relationship('UserProfile', back_populates='user', cascade='all, delete-orphan')
    preferences: Mapped[List['UserPreference']] = relationship('UserPreference', back_populates='user', cascade='all, delete-orphan')


class UserProfile(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'user_profiles'
    __table_args__ = (
        Index('ix_user_profiles_user_id', 'user_id'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)
    date_of_birth: Mapped[Optional[Date]] = mapped_column(Date)
    gender: Mapped[Optional[GenderEnum]] = mapped_column(SAEnum(GenderEnum, name='gender_enum'))
    college: Mapped[Optional[str]] = mapped_column(String)
    department: Mapped[Optional[str]] = mapped_column(String)
    year: Mapped[Optional[int]] = mapped_column(Integer)
    height_cm: Mapped[Optional[Numeric]] = mapped_column(Numeric(5, 2))
    weight_kg: Mapped[Optional[Numeric]] = mapped_column(Numeric(5, 2))
    blood_group: Mapped[Optional[str]] = mapped_column(String(5))
    ai_personality: Mapped[Optional[str]] = mapped_column(String)
    avatar_url: Mapped[Optional[str]] = mapped_column(String)
    timezone: Mapped[Optional[str]] = mapped_column(String)

    user = relationship('User', back_populates='profiles')


class UserPreference(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'user_preferences'
    __table_args__ = (
        Index('ix_user_prefs_user_id', 'user_id'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    theme: Mapped[Optional[str]] = mapped_column(String, default='calm')
    reminder_preferences: Mapped[dict] = mapped_column(JSON, default={})
    notification_preferences: Mapped[dict] = mapped_column(JSON, default={})
    language: Mapped[Optional[str]] = mapped_column(String, default='en')

    user = relationship('User', back_populates='preferences')
import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, JSON, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin, SoftDeleteMixin


gender_enum = ENUM('male', 'female', 'other', 'prefer_not_to_say', name='gender_enum', create_type=False)
provider_enum = ENUM('firebase','google','email','apple', name='provider_enum', create_type=False)


class User(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'users'
    email = Column(String, unique=True, nullable=False, index=True)
    primary_phone = Column(String)
    firebase_uid = Column(String, unique=True)

    profiles = relationship('UserProfile', back_populates='user', cascade='all, delete-orphan')
    preferences = relationship('UserPreferences', back_populates='user', uselist=False, cascade='all, delete-orphan')


class UserProfile(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'user_profiles'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(sa.Date)
    gender = Column(gender_enum)
    college = Column(String)
    department = Column(String)
    year = Column(Integer)
    height_cm = Column(sa.Numeric(5,2))
    weight_kg = Column(sa.Numeric(5,2))
    blood_group = Column(String(5))
    ai_personality = Column(String)
    avatar_url = Column(String)
    timezone = Column(String)

    user = relationship('User', back_populates='profiles')


class UserPreferences(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'user_preferences'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    theme = Column(String, default='calm')
    reminder_preferences = Column(JSON, default={})
    notification_preferences = Column(JSON, default={})
    language = Column(String, default='en')

    user = relationship('User', back_populates='preferences')


class UserSetting(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'user_settings'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    key = Column(String, nullable=False)
    value = Column(JSON)

    __table_args__ = (UniqueConstraint('user_id','key', name='uq_user_setting_user_key'),)


class AuthAccount(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'auth_accounts'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'))
    provider = Column(provider_enum, nullable=False)
    provider_id = Column(String)
    email_verified = Column(sa.Boolean, default=False)


class RefreshToken(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'refresh_tokens'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    token = Column(String, nullable=False)
    issued_at = Column(DateTime := sa.Column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now()))
    expires_at = Column(sa.TIMESTAMP(timezone=True))
    device_info = Column(JSON)
    ip_address = Column(sa.dialects.postgresql.INET)
    revoked_at = Column(sa.TIMESTAMP(timezone=True))


class LoginHistory(Base, IDMixin):
    __tablename__ = 'login_history'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    provider = Column(provider_enum)
    login_at = Column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    device_info = Column(JSON)
    ip_address = Column(sa.dialects.postgresql.INET)
    session_info = Column(JSON)
