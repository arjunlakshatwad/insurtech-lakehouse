{% snapshot snap_oracle_customers %}

{{
    config(
      target_schema='silver',
      unique_key='customer_id',
      strategy='timestamp',
      updated_at='updated_at'
    )
}}

select * from {{ source('oracle_bronze', 'oracle_customers') }}

{% endsnapshot %}