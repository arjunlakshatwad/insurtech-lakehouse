{{
    config(
        materialized='incremental',
        unique_key='policy_id',
        incremental_strategy='merge'
    )
}}
with policies as (
    select * from {{ source('oracle_bronze', 'oracle_policies') }}
)

select
    policy_id,
    customer_id,
    product_code,
    premium,
    start_date,
    end_date,
    status,
    updated_at
from policies
{% if is_incremental() %}
  where updated_at > (select max(updated_at) from {{ this }})
{% endif %}