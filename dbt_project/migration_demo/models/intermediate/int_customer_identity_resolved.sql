with oracle_customers as (select * from {{ ref('stg_oracle__customers') }}),
     pg_customers     as (select * from {{ ref('stg_pg__customers') }})

select
    {{ dbt_utils.generate_surrogate_key(['coalesce(o.customer_id::string, p.customer_id::string)']) }} as customer_sk,
    coalesce(o.customer_id, null)   as oracle_customer_id,
    coalesce(p.customer_id, null)   as pg_customer_id,
    coalesce(o.email, p.email)      as email,
    case when o.customer_id is not null and p.customer_id is not null then 'matched'
         when o.customer_id is not null then 'oracle_only'
         else 'lending_only' end    as match_status
from oracle_customers o
full outer join pg_customers p on o.email = p.email