ALTER TABLE public.device_info
ADD COLUMN IF NOT EXISTS today_energy_amount FLOAT8 DEFAULT 0
ADD COLUMN IF NOT EXISTS yesterday_energy_amount FLOAT8 DEFAULT 0;