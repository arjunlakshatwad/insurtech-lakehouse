with source as (
    select * from {{ source('oracle_bronze', 'oracle_customers') }}
)
select
    customer_id,
    trim(lower(name)) as customer_name,
    trim(lower(email))  as email,
    dob,
    address,
    segment,
    'oracle' as source_system,
    updated_at
from source
where customer_id is not null