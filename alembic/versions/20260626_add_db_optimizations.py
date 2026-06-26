"""Add soft-delete tracking, streaks, analytics fields, indexes, and views.

Revision ID: 20260626_add_db_optimizations
Revises: 
Create Date: 2026-06-26 00:00:00.000000

"""

from alembic import op

revision = '20260626_add_db_optimizations'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    for table_name in [
        'users', 'user_profiles', 'user_preferences', 'user_settings', 'auth_accounts',
        'refresh_tokens', 'water_goals', 'water_logs', 'sleep_logs', 'meal_logs',
        'period_cycles', 'journal_entries', 'goals', 'tasks', 'calendar_events',
        'applications', 'notifications', 'ai_memories', 'ai_recommendations',
        'ai_conversations', 'daily_metrics', 'weekly_metrics', 'monthly_metrics',
        'life_scores'
    ]:
        op.execute(f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_trigger WHERE tgname = 'trg_{table_name}_update_updated_at'
            ) THEN
                EXECUTE 'CREATE TRIGGER trg_{table_name}_update_updated_at BEFORE UPDATE ON {table_name} FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column()';
            END IF;
        END $$;
        """)

    for table_name in [
        'users', 'user_profiles', 'user_preferences', 'user_settings', 'auth_accounts',
        'refresh_tokens', 'water_goals', 'water_logs', 'sleep_logs', 'meal_logs',
        'period_cycles', 'journal_entries', 'goals', 'tasks', 'calendar_events',
        'applications', 'notifications', 'ai_memories', 'ai_recommendations',
        'ai_conversations', 'daily_metrics', 'weekly_metrics', 'monthly_metrics',
        'life_scores'
    ]:
        op.execute(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ")

    op.execute("""
    CREATE TABLE IF NOT EXISTS user_streaks (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
        study_streak INTEGER DEFAULT 0,
        water_streak INTEGER DEFAULT 0,
        coding_streak INTEGER DEFAULT 0,
        habit_streak INTEGER DEFAULT 0,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
    );
    """)

    op.execute("ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS student_roll_no TEXT")
    op.execute("ALTER TABLE user_profiles ADD CONSTRAINT chk_user_profiles_year CHECK (year IS NULL OR year BETWEEN 1 AND 5)")
    op.execute("ALTER TABLE sleep_scores ADD CONSTRAINT chk_sleep_scores_score CHECK (score IS NULL OR score BETWEEN 0 AND 100)")
    op.execute("ALTER TABLE sleep_logs ADD CONSTRAINT chk_sleep_logs_quality CHECK (quality IS NULL OR quality BETWEEN 1 AND 5)")
    op.execute("ALTER TABLE period_cycles ADD CONSTRAINT chk_period_cycles_pain_level CHECK (pain_level IS NULL OR pain_level BETWEEN 0 AND 10)")
    op.execute("ALTER TABLE interview_feedback ADD CONSTRAINT chk_interview_feedback_rating CHECK (rating IS NULL OR rating BETWEEN 1 AND 5)")
    op.execute("ALTER TABLE learning_sessions ADD CONSTRAINT chk_learning_sessions_confidence CHECK (confidence IS NULL OR confidence BETWEEN 1 AND 5)")
    op.execute("ALTER TABLE daily_metrics ADD COLUMN IF NOT EXISTS task_completion_rate NUMERIC(5,2)")
    op.execute("ALTER TABLE daily_metrics ADD COLUMN IF NOT EXISTS habit_completion_rate NUMERIC(5,2)")
    op.execute("ALTER TABLE daily_metrics ADD COLUMN IF NOT EXISTS journal_entries_count INTEGER DEFAULT 0")
    op.execute("ALTER TABLE daily_metrics ADD COLUMN IF NOT EXISTS sleep_duration_minutes INTEGER")
    op.execute("ALTER TABLE daily_metrics ADD COLUMN IF NOT EXISTS life_score NUMERIC(5,2)")
    op.execute("ALTER TABLE daily_metrics ADD CONSTRAINT chk_daily_metrics_task_completion_rate CHECK (task_completion_rate IS NULL OR task_completion_rate BETWEEN 0 AND 100)")
    op.execute("ALTER TABLE daily_metrics ADD CONSTRAINT chk_daily_metrics_habit_completion_rate CHECK (habit_completion_rate IS NULL OR habit_completion_rate BETWEEN 0 AND 100)")
    op.execute("ALTER TABLE daily_metrics ADD CONSTRAINT chk_daily_metrics_journal_entries_count CHECK (journal_entries_count IS NULL OR journal_entries_count >= 0)")

    op.execute("CREATE INDEX IF NOT EXISTS idx_user_streaks_user_id ON user_streaks (user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user_status ON tasks (user_id, status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_goals_user_status ON goals (user_id, status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_journal_entries_user_id ON journal_entries (user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user_status ON notifications (user_id, status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_mood_logs_user_id ON mood_logs (user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_calendar_events_owner_id ON calendar_events (owner_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_applications_user_id ON applications (user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_tasks_metadata_gin ON tasks USING GIN (metadata)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_goals_metadata_gin ON goals USING GIN (metadata)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_calendar_events_metadata_gin ON calendar_events USING GIN (metadata)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_applications_metadata_gin ON applications USING GIN (metadata)")

    op.execute("""
    CREATE MATERIALIZED VIEW IF NOT EXISTS mv_life_scores AS
    SELECT user_id, max(calculated_at) as last_calc, avg(score) as avg_score
    FROM life_scores
    GROUP BY user_id;
    """)

    op.execute("""
    CREATE MATERIALIZED VIEW IF NOT EXISTS mv_daily_summary AS
    SELECT user_id, metric_date, sleep_score, water_ml, mood_score, study_minutes, coding_minutes,
           task_completion_rate, habit_completion_rate, journal_entries_count, life_score
    FROM daily_metrics;
    """)

    op.execute("""
    CREATE MATERIALIZED VIEW IF NOT EXISTS mv_weekly_summary AS
    SELECT user_id, date_trunc('week', metric_date)::date AS week_start,
           avg(sleep_score) AS avg_sleep_score,
           avg(water_ml) AS avg_water_ml,
           avg(mood_score) AS avg_mood_score,
           sum(study_minutes) AS total_study_minutes
    FROM daily_metrics
    GROUP BY user_id, date_trunc('week', metric_date)::date;
    """)

    op.execute("""
    CREATE MATERIALIZED VIEW IF NOT EXISTS mv_monthly_summary AS
    SELECT user_id, date_trunc('month', metric_date)::date AS month_start,
           avg(sleep_score) AS avg_sleep_score,
           avg(water_ml) AS avg_water_ml,
           avg(mood_score) AS avg_mood_score,
           sum(study_minutes) AS total_study_minutes
    FROM daily_metrics
    GROUP BY user_id, date_trunc('month', metric_date)::date;
    """)

    op.execute("""
    CREATE MATERIALIZED VIEW IF NOT EXISTS mv_productivity_summary AS
    SELECT user_id,
           count(*) FILTER (WHERE status = 'done') AS completed_tasks,
           count(*) AS total_tasks
    FROM tasks
    GROUP BY user_id;
    """)

    op.execute("COMMENT ON TABLE users IS 'Stores application users'")
    op.execute("COMMENT ON COLUMN users.firebase_uid IS 'Firebase Authentication UID'")
    op.execute("COMMENT ON TABLE user_profiles IS 'Stores user profile details and roll number information'")
    op.execute("COMMENT ON TABLE user_streaks IS 'Stores study, water, coding and habit streak information'")
    op.execute("COMMENT ON TABLE daily_metrics IS 'Stores daily analytics used by dashboards and AI recommendations'")


def downgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_productivity_summary")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_monthly_summary")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_weekly_summary")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_daily_summary")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_life_scores")

    op.execute("DROP INDEX IF EXISTS idx_applications_metadata_gin")
    op.execute("DROP INDEX IF EXISTS idx_calendar_events_metadata_gin")
    op.execute("DROP INDEX IF EXISTS idx_goals_metadata_gin")
    op.execute("DROP INDEX IF EXISTS idx_tasks_metadata_gin")
    op.execute("DROP INDEX IF EXISTS idx_applications_user_id")
    op.execute("DROP INDEX IF EXISTS idx_calendar_events_owner_id")
    op.execute("DROP INDEX IF EXISTS idx_mood_logs_user_id")
    op.execute("DROP INDEX IF EXISTS idx_notifications_user_status")
    op.execute("DROP INDEX IF EXISTS idx_journal_entries_user_id")
    op.execute("DROP INDEX IF EXISTS idx_goals_user_status")
    op.execute("DROP INDEX IF EXISTS idx_tasks_user_status")
    op.execute("DROP INDEX IF EXISTS idx_user_streaks_user_id")

    op.execute("ALTER TABLE daily_metrics DROP CONSTRAINT IF EXISTS chk_daily_metrics_journal_entries_count")
    op.execute("ALTER TABLE daily_metrics DROP CONSTRAINT IF EXISTS chk_daily_metrics_habit_completion_rate")
    op.execute("ALTER TABLE daily_metrics DROP CONSTRAINT IF EXISTS chk_daily_metrics_task_completion_rate")
    op.execute("ALTER TABLE daily_metrics DROP COLUMN IF EXISTS life_score")
    op.execute("ALTER TABLE daily_metrics DROP COLUMN IF EXISTS sleep_duration_minutes")
    op.execute("ALTER TABLE daily_metrics DROP COLUMN IF EXISTS journal_entries_count")
    op.execute("ALTER TABLE daily_metrics DROP COLUMN IF EXISTS habit_completion_rate")
    op.execute("ALTER TABLE daily_metrics DROP COLUMN IF EXISTS task_completion_rate")

    op.execute("ALTER TABLE learning_sessions DROP CONSTRAINT IF EXISTS chk_learning_sessions_confidence")
    op.execute("ALTER TABLE interview_feedback DROP CONSTRAINT IF EXISTS chk_interview_feedback_rating")
    op.execute("ALTER TABLE period_cycles DROP CONSTRAINT IF EXISTS chk_period_cycles_pain_level")
    op.execute("ALTER TABLE sleep_logs DROP CONSTRAINT IF EXISTS chk_sleep_logs_quality")
    op.execute("ALTER TABLE sleep_scores DROP CONSTRAINT IF EXISTS chk_sleep_scores_score")
    op.execute("ALTER TABLE user_profiles DROP CONSTRAINT IF EXISTS chk_user_profiles_year")
    op.execute("ALTER TABLE user_profiles DROP COLUMN IF EXISTS student_roll_no")

    op.execute("DROP TABLE IF EXISTS user_streaks")

    for table_name in [
        'users', 'user_profiles', 'user_preferences', 'user_settings', 'auth_accounts',
        'refresh_tokens', 'water_goals', 'water_logs', 'sleep_logs', 'meal_logs',
        'period_cycles', 'journal_entries', 'goals', 'tasks', 'calendar_events',
        'applications', 'notifications', 'ai_memories', 'ai_recommendations',
        'ai_conversations', 'daily_metrics', 'weekly_metrics', 'monthly_metrics',
        'life_scores'
    ]:
        op.execute(f"ALTER TABLE {table_name} DROP COLUMN IF EXISTS deleted_at")

    op.execute("DROP FUNCTION IF EXISTS public.update_updated_at_column()")
