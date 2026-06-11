-- Deterministic demo dataset for the three core personas
INSERT INTO users (id, email, primary_phone, firebase_uid, created_at)
VALUES
  ('11111111-1111-1111-1111-111111111111','nhowmi05@gmail.com','+91 90000 50005','fb_nhowmi05', now()),
  ('22222222-2222-2222-2222-222222222222','ambikasoundharan@gmail.com','+91 90000 62206','fb_ambika_soundharan', now()),
  ('33333333-3333-3333-3333-333333333333','diviya2206@gmail.com','+91 90000 62206','fb_diviya_2206', now())
ON CONFLICT (id) DO NOTHING;

INSERT INTO user_profiles (id, user_id, first_name, last_name, college, department, year, timezone, ai_personality)
VALUES
  ('21111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Nhowmitha',NULL,'KGISL Institute of Technology','AI&DS',4,'Asia/Kolkata','structured'),
  ('22222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','Ambika',NULL,'KGISL Institute of Technology','AI&DS',4,'Asia/Kolkata','encouraging'),
  ('33333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Diviya',NULL,'KGISL Institute of Technology','AI&DS',4,'Asia/Kolkata','calm')
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
    SELECT generate_series(current_date - 6, current_date, interval '1 day')::date AS day
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

WITH days AS (
    SELECT generate_series(current_date - 6, current_date, interval '1 day')::date AS day
)
INSERT INTO sleep_logs (id, user_id, sleep_time, wake_time, duration_minutes, quality, notes)
SELECT (
       substr(md5('sleep-' || u.user_id::text || '-' || d.day::text), 1, 8) || '-' ||
       substr(md5('sleep-' || u.user_id::text || '-' || d.day::text), 9, 4) || '-' ||
       substr(md5('sleep-' || u.user_id::text || '-' || d.day::text), 13, 4) || '-' ||
       substr(md5('sleep-' || u.user_id::text || '-' || d.day::text), 17, 4) || '-' ||
       substr(md5('sleep-' || u.user_id::text || '-' || d.day::text), 21, 12)
     )::uuid,
       u.user_id,
       (d.day + time '23:15')::timestamp with time zone,
       (d.day + time '07:00')::timestamp with time zone + interval '1 day',
       u.duration_minutes,
       u.quality,
       u.notes
FROM days d
CROSS JOIN (VALUES
    ('11111111-1111-1111-1111-111111111111'::uuid, 465, 8, 'good focus next day'),
    ('22222222-2222-2222-2222-222222222222'::uuid, 420, 7, 'felt rested'),
    ('33333333-3333-3333-3333-333333333333'::uuid, 390, 6, 'late bedtime')
) AS u(user_id, duration_minutes, quality, notes);

WITH days AS (
    SELECT generate_series(current_date - 6, current_date, interval '1 day')::date AS day
)
INSERT INTO mood_logs (id, user_id, mood, intensity, notes, logged_at)
SELECT (
       substr(md5('mood-' || u.user_id::text || '-' || d.day::text), 1, 8) || '-' ||
       substr(md5('mood-' || u.user_id::text || '-' || d.day::text), 9, 4) || '-' ||
       substr(md5('mood-' || u.user_id::text || '-' || d.day::text), 13, 4) || '-' ||
       substr(md5('mood-' || u.user_id::text || '-' || d.day::text), 17, 4) || '-' ||
       substr(md5('mood-' || u.user_id::text || '-' || d.day::text), 21, 12)
     )::uuid,
       u.user_id,
       u.mood,
       u.intensity,
       u.notes,
       (d.day + time '21:00')::timestamp with time zone
FROM days d
CROSS JOIN (VALUES
    ('11111111-1111-1111-1111-111111111111'::uuid, 'calm'::mood_enum, 7, 'productive and calm'),
    ('22222222-2222-2222-2222-222222222222'::uuid, 'neutral'::mood_enum, 6, 'steady placement prep'),
    ('33333333-3333-3333-3333-333333333333'::uuid, 'stressed'::mood_enum, 5, 'heavy workload')
) AS u(user_id, mood, intensity, notes);

INSERT INTO journal_entries (id, user_id, title, content, mood, tags, created_at, updated_at)
VALUES
  ('81111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Weekly reset','I want to improve consistency this week.','calm','["planning","focus"]'::jsonb, now() - interval '2 days', now() - interval '2 days'),
  ('82222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','Interview prep','Practiced two mock questions today.','happy','["placements","confidence"]'::jsonb, now() - interval '1 day', now() - interval '1 day'),
  ('83333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Late night reflection','Need to sleep earlier and reduce scrolling.','stressed','["sleep","habit"]'::jsonb, now(), now())
ON CONFLICT (id) DO NOTHING;

INSERT INTO companies (id, name, website, industry)
VALUES
  ('91111111-1111-1111-1111-111111111111','Google','https://google.com','Technology'),
  ('92222222-1111-1111-1111-111111111111','Microsoft','https://microsoft.com','Technology'),
  ('93333333-1111-1111-1111-111111111111','Amazon','https://amazon.com','E-commerce')
ON CONFLICT (id) DO NOTHING;

INSERT INTO job_roles (id, company_id, title, description, location, level)
VALUES
  ('94111111-1111-1111-1111-111111111111','91111111-1111-1111-1111-111111111111','Software Engineer Intern','Backend and systems work','Remote','Intern'),
  ('94222222-1111-1111-1111-111111111111','92222222-1111-1111-1111-111111111111','Data Analyst Intern','Insights and reporting','Hyderabad','Intern'),
  ('94333333-1111-1111-1111-111111111111','93333333-1111-1111-1111-111111111111','Cloud Support Associate','Customer-facing support role','Bengaluru','Entry')
ON CONFLICT (id) DO NOTHING;

INSERT INTO applications (id, user_id, company_id, role_id, status, applied_at, metadata)
VALUES
  ('95111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','91111111-1111-1111-1111-111111111111','94111111-1111-1111-1111-111111111111','shortlisted',now() - interval '10 days','{"source": "career portal"}'::jsonb),
  ('95222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','92222222-1111-1111-1111-111111111111','94222222-1111-1111-1111-111111111111','applied',now() - interval '5 days','{"source": "referral"}'::jsonb),
  ('95333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','93333333-1111-1111-1111-111111111111','94333333-1111-1111-1111-111111111111','assessment',now() - interval '2 days','{"source": "college drive"}'::jsonb)
ON CONFLICT (id) DO NOTHING;

INSERT INTO notifications (id, user_id, message, scheduled_at, sent_at, status, created_at)
VALUES
  ('96111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Drink water and stretch', now() - interval '1 hour', now() - interval '1 hour', 'sent', now() - interval '1 hour'),
  ('96222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','Your interview is tomorrow', now() + interval '6 hours', NULL, 'pending', now()),
  ('96333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Write today''s journal entry', now() - interval '20 minutes', now() - interval '20 minutes', 'delivered', now() - interval '20 minutes')
ON CONFLICT (id) DO NOTHING;

INSERT INTO ai_memories (id, user_id, memory_type, content, metadata, embedding_id, created_at)
VALUES
  ('97111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','preference','prefers structured plans','{"priority": "morning"}'::jsonb,'mem-n-001', now() - interval '3 days'),
  ('97222222-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','goal','wants placement reminders','{"focus": "placements"}'::jsonb,'mem-a-001', now() - interval '2 days'),
  ('97333333-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','wellness','needs sleep nudges','{"focus": "sleep"}'::jsonb,'mem-d-001', now() - interval '1 day')
ON CONFLICT (id) DO NOTHING;

INSERT INTO daily_metrics (id, user_id, metric_date, sleep_score, water_ml, mood_score, study_minutes, coding_minutes)
VALUES
  ('98111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111', current_date - 2, 82, 2400, 7.5, 90, 60),
  ('98222222-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111', current_date - 1, 88, 2500, 8.0, 120, 75),
  ('98333333-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222', current_date - 1, 76, 2100, 7.2, 150, 45),
  ('98444444-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333', current_date - 1, 69, 1800, 6.4, 75, 30)
ON CONFLICT (user_id, metric_date) DO NOTHING;

INSERT INTO period_cycles (id, user_id, start_date, end_date, flow, pain_level, notes)
VALUES
  ('99111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111', current_date - 11, current_date - 6, 'medium', 3, 'mild symptoms'),
  ('99222222-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333', current_date - 18, current_date - 13, 'light', 2, 'shorter cycle')
ON CONFLICT (id) DO NOTHING;

INSERT INTO period_predictions (id, user_id, predicted_start, predicted_end, ovulation_date, pms_window, confidence, generated_at)
VALUES
  ('99333333-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111', current_date + 16, current_date + 21, current_date + 18, '{"start": "2026-06-27", "end": "2026-07-01"}'::jsonb, 0.842, now()),
  ('99444444-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333', current_date + 12, current_date + 17, current_date + 14, '{"start": "2026-06-23", "end": "2026-06-27"}'::jsonb, 0.778, now())
ON CONFLICT (id) DO NOTHING;

INSERT INTO journal_tags (id, name)
VALUES
  ('a1111111-1111-1111-1111-111111111111','planning'),
  ('a2222222-1111-1111-1111-111111111111','focus'),
  ('a3333333-1111-1111-1111-111111111111','placements'),
  ('a4444444-1111-1111-1111-111111111111','sleep')
ON CONFLICT (id) DO NOTHING;

INSERT INTO journal_entry_tags (journal_entry_id, tag_id)
VALUES
  ('81111111-1111-1111-1111-111111111111','a1111111-1111-1111-1111-111111111111'),
  ('81111111-1111-1111-1111-111111111111','a2222222-1111-1111-1111-111111111111'),
  ('82222222-1111-1111-1111-111111111111','a3333333-1111-1111-1111-111111111111'),
  ('83333333-1111-1111-1111-111111111111','a4444444-1111-1111-1111-111111111111')
ON CONFLICT DO NOTHING;

INSERT INTO journal_ai_analysis (id, journal_entry_id, ai_summary, ai_reflection, ai_suggestions, created_at)
VALUES
  ('b1111111-1111-1111-1111-111111111111','81111111-1111-1111-1111-111111111111','Weekly reset detected','You are building consistency and should protect your morning routine.','["Keep the same wake-up time", "Plan tasks the night before"]'::jsonb, now() - interval '2 days'),
  ('b2222222-1111-1111-1111-111111111111','82222222-1111-1111-1111-111111111111','Interview prep improving','Confidence is growing from repeated practice.','["Do one mock interview", "Review one company profile"]'::jsonb, now() - interval '1 day')
ON CONFLICT (id) DO NOTHING;

INSERT INTO task_reminders (id, task_id, reminder_at, method, created_at)
VALUES
  ('c1111111-1111-1111-1111-111111111111','71111111-1111-1111-1111-111111111111', now() + interval '2 days', 'push', now()),
  ('c2222222-1111-1111-1111-111111111111','72222222-1111-1111-1111-111111111111', now() + interval '1 day', 'push', now()),
  ('c3333333-1111-1111-1111-111111111111','74444444-1111-1111-1111-111111111111', now() + interval '12 hours', 'email', now())
ON CONFLICT (id) DO NOTHING;

INSERT INTO task_comments (id, task_id, user_id, comment, created_at)
VALUES
  ('c4444444-1111-1111-1111-111111111111','71111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Need to check index coverage before demo', now() - interval '1 day'),
  ('c5555555-1111-1111-1111-111111111111','73333333-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','Looks ready to submit', now() - interval '1 day')
ON CONFLICT (id) DO NOTHING;

INSERT INTO event_categories (id, name)
VALUES
  ('d1111111-1111-1111-1111-111111111111','study'),
  ('d2222222-1111-1111-1111-111111111111','assessment'),
  ('d3333333-1111-1111-1111-111111111111','health')
ON CONFLICT (id) DO NOTHING;

INSERT INTO calendar_events (id, owner_id, title, description, event_type, start_at, end_at, location, recurring_rule, metadata)
VALUES
  ('d4444444-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Morning study block','Deep work for DSA practice','study',now() + interval '2 hours',now() + interval '3 hours','Library','FREQ=DAILY','{"focus": "coding"}'::jsonb),
  ('d5555555-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','Placement assessment','Online aptitude test','assessment',now() + interval '1 day',now() + interval '1 day 1 hour','Remote',NULL,'{"company": "Microsoft"}'::jsonb),
  ('d6666666-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Health check-in','Mood and sleep review','health',now() + interval '4 hours',now() + interval '4 hours 30 minutes','Home',NULL,'{"type": "checkin"}'::jsonb)
ON CONFLICT (id) DO NOTHING;

INSERT INTO event_participants (event_id, user_id, role, status)
VALUES
  ('d4444444-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','owner','accepted'),
  ('d4444444-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','participant','accepted'),
  ('d5555555-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','owner','accepted'),
  ('d6666666-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','owner','accepted')
ON CONFLICT DO NOTHING;

INSERT INTO squads (id, name, description, is_private)
VALUES
  ('e1111111-1111-1111-1111-111111111111','Placement Pals','Daily placement and study accountability group',false),
  ('e2222222-1111-1111-1111-111111111111','Wellness Circle','Supportive health tracking and habit sharing',false)
ON CONFLICT (id) DO NOTHING;

INSERT INTO squad_members (squad_id, user_id, role, joined_at)
VALUES
  ('e1111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','admin',now() - interval '10 days'),
  ('e1111111-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','member',now() - interval '9 days'),
  ('e1111111-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','member',now() - interval '8 days'),
  ('e2222222-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','member',now() - interval '7 days'),
  ('e2222222-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','admin',now() - interval '6 days')
ON CONFLICT DO NOTHING;

INSERT INTO squad_goals (id, squad_id, title, description, created_at)
VALUES
  ('f1111111-1111-1111-1111-111111111111','e1111111-1111-1111-1111-111111111111','Weekly streak','Everyone completes at least 5 productive days', now() - interval '9 days'),
  ('f2222222-1111-1111-1111-111111111111','e2222222-1111-1111-1111-111111111111','Share wellness wins','Post one sleep or mood improvement every week', now() - interval '5 days')
ON CONFLICT (id) DO NOTHING;

INSERT INTO squad_challenges (id, squad_id, title, details, start_date, end_date)
VALUES
  ('f3333333-1111-1111-1111-111111111111','e1111111-1111-1111-1111-111111111111','7-day DSA Sprint','Solve one problem per day', current_date - 2, current_date + 5),
  ('f4444444-1111-1111-1111-111111111111','e2222222-1111-1111-1111-111111111111','Sleep Before 11','Track a full week of early sleep', current_date - 1, current_date + 6)
ON CONFLICT (id) DO NOTHING;

INSERT INTO squad_challenge_progress (id, challenge_id, user_id, progress, recorded_at)
VALUES
  ('f5555555-1111-1111-1111-111111111111','f3333333-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','{"completed_days": 3}'::jsonb, now() - interval '1 day'),
  ('f6666666-1111-1111-1111-111111111111','f4444444-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','{"completed_days": 2}'::jsonb, now() - interval '1 day')
ON CONFLICT (id) DO NOTHING;

INSERT INTO subjects (id, user_id, name, description)
VALUES
  ('g3333333-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111','Data Structures','Core DSA preparation'),
  ('g4444444-1111-1111-1111-111111111111','22222222-2222-2222-2222-222222222222','Aptitude','Placement aptitude practice'),
  ('g5555555-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Wellness habits','Sleep, mood and journaling focus')
ON CONFLICT (id) DO NOTHING;

INSERT INTO learning_sessions (id, subject_id, topic, duration_minutes, confidence, notes, started_at, ended_at)
VALUES
  ('g6666666-1111-1111-1111-111111111111','g3333333-1111-1111-1111-111111111111','Arrays and strings', 60, 8, 'Strong recall', now() - interval '1 day 3 hours', now() - interval '1 day 2 hours'),
  ('g7777777-1111-1111-1111-111111111111','g4444444-1111-1111-1111-111111111111','Logical reasoning', 45, 7, 'Needs more speed', now() - interval '2 days 4 hours', now() - interval '2 days 3 hours'),
  ('g8888888-1111-1111-1111-111111111111','g5555555-1111-1111-1111-111111111111','Habit check-in', 30, 9, 'Very reflective', now() - interval '1 day 5 hours', now() - interval '1 day 4 hours')
ON CONFLICT (id) DO NOTHING;

INSERT INTO learning_progress (id, subject_id, progress_percent, recorded_at)
VALUES
  ('g9999999-1111-1111-1111-111111111111','g3333333-1111-1111-1111-111111111111', 42.5, now() - interval '1 day'),
  ('h1111111-1111-1111-1111-111111111111','g4444444-1111-1111-1111-111111111111', 58.0, now() - interval '2 days'),
  ('h2222222-1111-1111-1111-111111111111','g5555555-1111-1111-1111-111111111111', 66.0, now() - interval '1 day')
ON CONFLICT (id) DO NOTHING;
