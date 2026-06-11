import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, IDMixin, TimestampMixin


class DailyMetric(Base, IDMixin, TimestampMixin):
    __tablename__ = 'daily_metrics'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'))
    metric_date = Column(sa.Date, nullable=False)
    sleep_score = Column(sa.Numeric)
    water_ml = Column(sa.Integer)
    mood_score = Column(sa.Numeric)
    study_minutes = Column(sa.Integer)
    coding_minutes = Column(sa.Integer)

    __table_args__ = (sa.UniqueConstraint('user_id','metric_date', name='uq_daily_metric_user_date'),)


class WeeklyMetric(Base, IDMixin, TimestampMixin):
    __tablename__ = 'weekly_metrics'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'))
    week_start = Column(sa.Date, nullable=False)
    metrics = Column(sa.JSON)

    __table_args__ = (sa.UniqueConstraint('user_id','week_start', name='uq_weekly_metric_user_week'),)


class MonthlyMetric(Base, IDMixin, TimestampMixin):
    __tablename__ = 'monthly_metrics'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'))
    month_start = Column(sa.Date, nullable=False)
    metrics = Column(sa.JSON)

    __table_args__ = (sa.UniqueConstraint('user_id','month_start', name='uq_monthly_metric_user_month'),)


class LifeScore(Base, IDMixin, TimestampMixin):
    __tablename__ = 'life_scores'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'))
    score = Column(sa.Numeric)
    components = Column(sa.JSON)
