-- Seed users and core demo data for the DearMe personas
-- This version keeps deterministic IDs for repeatable local development and stores
-- roll numbers in the profile table instead of in the users table.

INSERT INTO users (id, email, primary_phone, firebase_uid, created_at)
VALUES
<<<<<<< HEAD
  ('11111111-1111-1111-1111-111111111111','nhowmi05@gmail.com','+91 90000 50005','fb_nhowmi05', now()),
  ('22222222-2222-2222-2222-222222222222','ambikasoundharan@gmail.com','+91 90000 62206','fb_ambika_soundharan', now()),
  ('33333333-3333-3333-3333-333333333333','diviya2206@gmail.com','+91 90000 62206','fb_diviya_2206', now())
ON CONFLICT (id) DO NOTHING;

INSERT INTO user_profiles (id, user_id, first_name, last_name, college, department, year, timezone, ai_personality, student_roll_no)
VALUES
  ('21111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Nhowmitha',NULL,'KGISL Institute of Technology','AI&DS',4,'Asia/Kolkata','structured','23AIA63'),
  ('22222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','Ambika',NULL,'KGISL Institute of Technology','AI&DS',4,'Asia/Kolkata','encouraging','23AIA06'),
  ('33333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Diviya',NULL,'KGISL Institute of Technology','AI&DS',4,'Asia/Kolkata','calm','23AIA21')
ON CONFLICT (id) DO NOTHING;

INSERT INTO user_preferences (id, user_id, theme, reminder_preferences, notification_preferences, language)
VALUES
  ('31111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','calm','{"water": true, "sleep": true, "goals": true}'::jsonb,'{"push": true, "email": false}'::jsonb,'en'),
  ('32222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','focus','{"study": true, "placements": true}'::jsonb,'{"push": true, "email": true}'::jsonb,'en'),
  ('33333333-2222-2222-2222-111111111111','33333333-3333-3333-3333-333333333333','gentle','{"journal": true, "mood": true}'::jsonb,'{"push": true, "email": false}'::jsonb,'en')
ON CONFLICT (id) DO NOTHING;

INSERT INTO user_settings (id, user_id, key, value)
VALUES
  ('34111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','internal_seed_metadata','{"roll_number": "23AIA63", "source": "seed_only"}'::jsonb),
  ('34222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','internal_seed_metadata','{"roll_number": "23AIA06", "source": "seed_only"}'::jsonb),
  ('34333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','internal_seed_metadata','{"roll_number": "23AIA21", "source": "seed_only"}'::jsonb)
ON CONFLICT (id) DO NOTHING;

INSERT INTO auth_accounts (id, user_id, provider, provider_id, email_verified)
VALUES
  ('41111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','firebase','fb_nhowmitha', true),
  ('42222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','firebase','fb_ambika', true),
  ('43333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','firebase','fb_diviya', true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO water_goals (id, user_id, daily_goal_ml, effective_date)
VALUES
  ('51111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111',2500,current_date),
  ('52222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222',2200,current_date),
  ('53333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333',2000,current_date)
ON CONFLICT (id) DO NOTHING;

INSERT INTO goals (id, user_id, title, description, category, target_value, current_value, start_date, end_date, status, metadata)
VALUES
  ('61111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Build a daily study streak','Study every day for 30 minutes','productivity',30,12,current_date - 29,current_date + 1,'in_progress','{"priority": "high"}'::jsonb),
  ('62222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','Apply to internships','Submit applications and track progress','placements',10,4,current_date - 20,current_date + 40,'in_progress','{"deadline": "next month"}'::jsonb),
  ('63333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Improve wellness routine','Sleep on time and log mood daily','health',21,9,current_date - 21,current_date + 7,'in_progress','{"focus": "sleep"}'::jsonb)
ON CONFLICT (id) DO NOTHING;

INSERT INTO task_categories (id, name)
VALUES
  ('70111111-1111-1111-1111-111111111111','productivity'),
  ('70222222-1111-1111-1111-111111111111','placements'),
  ('70333333-1111-1111-1111-111111111111','health')
ON CONFLICT (id) DO NOTHING;

INSERT INTO tasks (id, user_id, title, description, priority, status, due_date, completed_at, category_id, metadata)
VALUES
  ('71111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Review DB schema','Audit tables and indexes before release','high','todo',now() + interval '2 days',NULL,'70111111-1111-1111-1111-111111111111','{"module": "database"}'::jsonb),
  ('72222222-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Complete one coding problem','Practice array and string patterns','medium','in_progress',now() + interval '1 day',NULL,'70111111-1111-1111-1111-111111111111','{"module": "learning"}'::jsonb),
  ('73333333-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','Submit resume draft','Finalize and upload placement resume','high','done',now() - interval '1 day',now() - interval '1 day','70222222-1111-1111-1111-111111111111','{"module": "placements"}'::jsonb),
  ('74444444-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Plan tomorrow','Create a focused plan for the next day','medium','todo',now() + interval '12 hours',NULL,'70111111-1111-1111-1111-111111111111','{"module": "planning"}'::jsonb)
ON CONFLICT (id) DO NOTHING;

WITH days AS (
    SELECT generate_series(current_date - 2, current_date, interval '1 day')::date AS day
)
INSERT INTO water_logs (id, user_id, amount_ml, logged_at, notes)
SELECT (
       substr(md5('water-' || u.user_id::text || '-' || d.day::text), 1, 8) || '-' ||
       substr(md5('water-' || u.user_id::text || '-' || d.day::text), 9, 4) || '-' ||
       substr(md5('water-' || u.user_id::text || '-' || d.day::text), 13, 4) || '-' ||
       substr(md5('water-' || u.user_id::text || '-' || d.day::text), 17, 4) || '-' ||
       substr(md5('water-' || u.user_id::text || '-' || d.day::text), 21, 12)
     )::uuid,
       u.user_id,
       u.amount_ml,
       (d.day + time '08:00')::timestamp with time zone,
       u.notes
FROM days d
CROSS JOIN (VALUES
    ('11111111-1111-1111-1111-111111111111'::uuid, 2400, 'morning target met'),
    ('22222222-2222-2222-2222-222222222222'::uuid, 2100, 'midday refill'),
    ('33333333-3333-3333-3333-333333333333'::uuid, 1800, 'steady hydration')
) AS u(user_id, amount_ml, notes);

INSERT INTO journal_entries (id, user_id, title, content, mood, tags, created_at, updated_at)
VALUES
  ('81111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Weekly reset','I want to improve consistency this week.','calm','["planning","focus"]'::jsonb, now() - interval '2 days', now() - interval '2 days'),
  ('82222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','Interview prep','Practiced two mock questions today.','happy','["placements","confidence"]'::jsonb, now() - interval '1 day', now() - interval '1 day'),
  ('83333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Late night reflection','Need to sleep earlier and reduce scrolling.','stressed','["sleep","habit"]'::jsonb, now(), now())
ON CONFLICT (id) DO NOTHING;

INSERT INTO daily_metrics (id, user_id, metric_date, sleep_score, water_ml, mood_score, study_minutes, coding_minutes)
VALUES
  ('98111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111', current_date - 2, 82, 2400, 7.5, 90, 60),
  ('98222222-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111', current_date - 1, 88, 2500, 8.0, 120, 75),
  ('98333333-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222', current_date - 1, 76, 2100, 7.2, 150, 45),
  ('98444444-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333', current_date - 1, 69, 1800, 6.4, 75, 30)
ON CONFLICT (user_id, metric_date) DO NOTHING;

=======
  ('11111111-1111-1111-1111-111111111111','Nhowmitha','S','Example College','AIDS',4),
  ('22222222-2222-2222-2222-222222222222','Ambika','S','Example College','AIDS',4),
  ('33333333-3333-3333-3333-333333333333','Diviya','V','Example College','AIDS',4)
ON CONFLICT DO NOTHING;
>>>>>>> 6848afa (added ai mem)
