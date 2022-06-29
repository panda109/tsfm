
create table public.device_data(
id SERIAL NOT NULL PRIMARY KEY,
dev_uuid VARCHAR NOT NULL,
scope VARCHAR,
model VARCHAR,
value FLOAT8,
generated_time INT8,
uploaded_time INT8
);

create table public.device_info(
id SERIAL NOT NULL PRIMARY KEY,
uuid VARCHAR UNIQUE, 
name VARCHAR,
model VARCHAR,
online_status VARCHAR,
gw_uuid VARCHAR,
gw_status VARCHAR,
user_id  VARCHAR,
associated VARCHAR,
target_energy_level FLOAT8 DEFAULT 5,
lower_bound INT DEFAULT 10,
start_time INT DEFAULT 7,
end_time INT DEFAULT 18,
notify VARCHAR DEFAULT 'ON',
group_id VARCHAR DEFAULT '0',
group_lower_bound INT DEFAULT 5000,
weekly_energy_amount FLOAT8 DEFAULT 0,
monthly_energy_amount FLOAT8 DEFAULT 0,
annual_energy_amount FLOAT8 DEFAULT 0
);

create table public.user_mgmt(
id SERIAL NOT NULL PRIMARY KEY,
user_id VARCHAR UNIQUE,
username VARCHAR,
email VARCHAR,
activated VARCHAR,
notify_all VARCHAR DEFAULT 'ON'
);


create table public.rules(
id SERIAL NOT NULL PRIMARY KEY,
name VARCHAR,
dev_uuid VARCHAR,
rule_info TEXT
);

create table public.notifications(
id SERIAL NOT NULL PRIMARY KEY,
user_id VARCHAR,
rule_id INT,
published BOOL,
scheduled_time TIMESTAMP(3) WITHOUT TIME ZONE,
content TEXT
);

create table public.posts(
id SERIAL NOT NULL PRIMARY KEY,
user_id  VARCHAR,
rule_id INT,
published BOOL,
scheduled_time TIMESTAMP(3) WITHOUT TIME ZONE,
content TEXT
);