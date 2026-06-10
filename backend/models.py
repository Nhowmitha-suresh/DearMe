"""SQLAlchemy models for DearMe (representative subset)."""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, func, JSON
from sqlalchemy.dialects.postgresql import UUID, ENUM, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

Base = declarative_base()

def gen_uuid():
    return sa.text('gen_random_uuid()')

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=gen_uuid())
    email = Column(String, unique=True, nullable=False)
    primary_phone = Column(String)
    firebase_uid = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=gen_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(sa.Date)
    gender = Column(ENUM('male','female','other','prefer_not_to_say', name='gender_enum'))
    college = Column(String)
    department = Column(String)
    year = Column(Integer)
    height_cm = Column(sa.Numeric(5,2))
    weight_kg = Column(sa.Numeric(5,2))
    blood_group = Column(String(5))
    ai_personality = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

class WaterLog(Base):
    __tablename__ = 'water_logs'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=gen_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    amount_ml = Column(Integer, nullable=False)
    logged_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=gen_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    target_value = Column(sa.Numeric)
    current_value = Column(sa.Numeric, default=0)
    status = Column(ENUM('not_started','in_progress','paused','completed','abandoned', name='goal_status_enum'), server_default='not_started')
