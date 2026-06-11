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
    primary_phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    firebase_uid: Mapped[Optional[str]] = mapped_column(String, unique=True)

    profiles: Mapped[List['UserProfile']] = relationship('UserProfile', back_populates='user', cascade='all, delete-orphan')
    preferences: Mapped[List['UserPreference']] = relationship('UserPreference', back_populates='user', cascade='all, delete-orphan')


from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Date, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import INET, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, Base, GenderEnum, IDMixin, ProviderEnum, SoftDeleteMixin


class User(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'users'
    __table_args__ = (Index('ix_users_email', 'email'),)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    primary_phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    firebase_uid: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)

    profiles: Mapped[list['UserProfile']] = relationship(
        'UserProfile', back_populates='user', cascade='all, delete-orphan'
    )
    preferences: Mapped[Optional['UserPreference']] = relationship(
        'UserPreference', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )
    auth_accounts: Mapped[list['AuthAccount']] = relationship(
        'AuthAccount', back_populates='user', cascade='all, delete-orphan'
    )
    refresh_tokens: Mapped[list['RefreshToken']] = relationship(
        'RefreshToken', back_populates='user', cascade='all, delete-orphan'
    )
    login_history: Mapped[list['LoginHistory']] = relationship(
        'LoginHistory', back_populates='user', cascade='all, delete-orphan'
    )


class UserProfile(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'user_profiles'
    __table_args__ = (Index('ix_user_profiles_user_id', 'user_id'),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),  # type: ignore[arg-type]
        nullable=False,
    )
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[GenderEnum]] = mapped_column(SAEnum(GenderEnum, name='gender_enum'), nullable=True)
    college: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    height_cm: Mapped[Optional[float]] = mapped_column(nullable=True)
    weight_kg: Mapped[Optional[float]] = mapped_column(nullable=True)
    blood_group: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    ai_personality: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user: Mapped['User'] = relationship('User', back_populates='profiles')


class UserPreference(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'user_preferences'
    __table_args__ = (Index('ix_user_preferences_user_id', 'user_id'),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),  # type: ignore[arg-type]
        unique=True,
        nullable=False,
    )
    theme: Mapped[Optional[str]] = mapped_column(String, default='calm', nullable=True)
    reminder_preferences: Mapped[dict] = mapped_column(JSON, default=dict)
    notification_preferences: Mapped[dict] = mapped_column(JSON, default=dict)
    language: Mapped[Optional[str]] = mapped_column(String, default='en', nullable=True)

    user: Mapped['User'] = relationship('User', back_populates='preferences')


UserPreferences = UserPreference


class UserSetting(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'user_settings'
    __table_args__ = (UniqueConstraint('user_id', 'key', name='uq_user_setting_user_key'),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),  # type: ignore[arg-type]
        nullable=False,
    )
    key: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class AuthAccount(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'auth_accounts'
    __table_args__ = (Index('ix_auth_accounts_user_id', 'user_id'),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),  # type: ignore[arg-type]
        nullable=False,
    )
    provider: Mapped[ProviderEnum] = mapped_column(SAEnum(ProviderEnum, name='provider_enum'), nullable=False)
    provider_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='auth_accounts')


class RefreshToken(Base, IDMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'refresh_tokens'
    __table_args__ = (Index('ix_refresh_tokens_user_id', 'user_id'),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),  # type: ignore[arg-type]
        nullable=False,
    )
    token: Mapped[str] = mapped_column(Text, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    device_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(INET, nullable=True)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped['User'] = relationship('User', back_populates='refresh_tokens')


class LoginHistory(Base, IDMixin):
    __tablename__ = 'login_history'
    __table_args__ = (Index('ix_login_history_user_id', 'user_id'),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),  # type: ignore[arg-type]
        nullable=False,
    )
    provider: Mapped[Optional[ProviderEnum]] = mapped_column(SAEnum(ProviderEnum, name='provider_enum'), nullable=True)
    login_at: Mapped[datetime] = mapped_column(nullable=False)
    device_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(INET, nullable=True)
    session_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    user: Mapped['User'] = relationship('User', back_populates='login_history')
