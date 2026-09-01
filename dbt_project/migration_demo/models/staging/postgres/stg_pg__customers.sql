with source as (
    select * from {{ source('pg_bronze', 'pg_customers') }}
)
select
    customer_id,
    trim(lower(email)) as email,
    kyc_status,
    'postgres' as source_system,
    updated_at
from source
where customer_id is not null