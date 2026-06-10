-- Seed users and basic data for Nhowmitha, Ambika, Diviya
INSERT INTO users (id, email, primary_phone, firebase_uid, created_at) VALUES
  ('11111111-1111-1111-1111-111111111111','nhowmitha@example.com','+911234567890','fb_nhowmitha', now()),
  ('22222222-2222-2222-2222-222222222222','ambika@example.com','+911234567891','fb_ambika', now()),
  ('33333333-3333-3333-3333-333333333333','diviya@example.com','+911234567892','fb_diviya', now())
ON CONFLICT (email) DO NOTHING;

-- Basic profiles
INSERT INTO user_profiles (user_id, first_name, last_name, college, department, year)
VALUES
  ('11111111-1111-1111-1111-111111111111','Nhowmitha','K','Example College','CSE',3),
  ('22222222-2222-2222-2222-222222222222','Ambika','R','Example College','ECE',4),
  ('33333333-3333-3333-3333-333333333333','Diviya','S','Example College','IT',2)
ON CONFLICT DO NOTHING;
