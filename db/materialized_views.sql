-- Materialized views for analytics
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_daily_summary AS
SELECT dm.user_id,
       dm.metric_date,
       dm.sleep_score,
       dm.water_ml,
       dm.mood_score,
       dm.study_minutes,
       dm.coding_minutes
FROM daily_metrics dm;

CREATE INDEX IF NOT EXISTS idx_mv_daily_summary_user_date ON mv_daily_summary (user_id, metric_date);

CREATE MATERIALIZED VIEW IF NOT EXISTS mv_user_goal_task_summary AS
SELECT u.id AS user_id,
       u.email,
       COALESCE(g.goal_count, 0) AS goal_count,
       COALESCE(g.active_goals, 0) AS active_goals,
       COALESCE(t.open_tasks, 0) AS open_tasks,
       COALESCE(t.overdue_tasks, 0) AS overdue_tasks
FROM users u
LEFT JOIN (
    SELECT user_id,
           count(*) AS goal_count,
           count(*) FILTER (WHERE status IN ('not_started', 'in_progress', 'paused')) AS active_goals
    FROM goals
    GROUP BY user_id
) g ON g.user_id = u.id
LEFT JOIN (
    SELECT user_id,
           count(*) FILTER (WHERE status IN ('todo', 'in_progress', 'blocked')) AS open_tasks,
           count(*) FILTER (WHERE status IN ('todo', 'in_progress', 'blocked') AND due_date < now()) AS overdue_tasks
    FROM tasks
    GROUP BY user_id
) t ON t.user_id = u.id;

CREATE MATERIALIZED VIEW IF NOT EXISTS mv_upcoming_schedule AS
SELECT owner_id AS user_id,
       date_trunc('day', start_at) AS schedule_day,
       count(*) AS event_count,
       min(start_at) AS next_event_at
FROM calendar_events
WHERE start_at >= now() - interval '1 day'
GROUP BY owner_id, date_trunc('day', start_at);

CREATE INDEX IF NOT EXISTS idx_mv_user_goal_task_summary_user_id ON mv_user_goal_task_summary (user_id);
CREATE INDEX IF NOT EXISTS idx_mv_upcoming_schedule_user_day ON mv_upcoming_schedule (user_id, schedule_day);
