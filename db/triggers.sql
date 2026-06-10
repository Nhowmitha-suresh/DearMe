-- Triggers and helper functions (separate file)
CREATE OR REPLACE FUNCTION public.set_created_at()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    NEW.created_at = COALESCE(NEW.created_at, now());
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach set_created_at to tables without created_at default behavior if needed.
