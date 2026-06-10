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
