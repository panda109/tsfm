ALTER TABLE public.device_info
ADD COLUMN IF NOT EXISTS instance_power FLOAT8 DEFAULT 0,
ADD COLUMN IF NOT EXISTS instance_power_generated_time INT8 DEFAULT 0;
