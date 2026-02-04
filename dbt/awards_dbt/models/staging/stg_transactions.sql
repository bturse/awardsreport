{{ config(materialized='table') }}

with assistance as (
    select
        'assistance' as source_table,
        assistance_transaction_unique_key as transaction_unique_key,
        assistance_award_unique_key as award_summary_unique_key,
        usaspending_permalink,
        action_date,
        awarding_agency_name,
        cfda_number,
        cfda_title,
        null::text as naics_code,
        null::text as naics_description,
        null::text as product_or_service_code,
        null::text as product_or_service_code_description,
        recipient_uei,
        recipient_name,
        case
            when assistance_type_code in ('07','08')
                then coalesce(original_loan_subsidy_cost, 0.0)
            else coalesce(federal_action_obligation, 0.0)
        end as generated_pragmatic_obligations
    from {{ source('raw', 'assistance_transactions') }}
),
procurement as (
    select
        'procurement' as source_table,
        contract_transaction_unique_key as transaction_unique_key,
        contract_award_unique_key as award_summary_unique_key,
        usaspending_permalink,
        action_date,
        awarding_agency_name,
        null::text as cfda_number,
        null::text as cfda_title,
        naics_code,
        naics_description,
        product_or_service_code,
        product_or_service_code_description,
        recipient_uei,
        recipient_name,
        coalesce(federal_action_obligation, 0.0) as generated_pragmatic_obligations
    from {{ source('raw', 'procurement_transactions') }}
)
select * from assistance
union all
select * from procurement