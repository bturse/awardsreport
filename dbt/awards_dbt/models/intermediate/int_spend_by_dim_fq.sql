with base as (
    select
        {{ fiscal_year('action_date') }}    as fiscal_year,
        {{ fiscal_quarter('action_date') }} as fiscal_quarter,

        source_table,
        generated_pragmatic_obligations as obligations,

        -- dims we may pivot into long form
        award_summary_unique_key,
        usaspending_permalink,

        awarding_agency_name,

        cfda_number,
        cfda_title,

        naics_code,
        naics_description,

        product_or_service_code,
        product_or_service_code_description,

        recipient_uei,
        recipient_name

    from {{ ref('stg_transactions') }}
),

long as (

    -- award
    select
        fiscal_year,
        fiscal_quarter,
        source_table,
        'award' as dim_type,
        award_summary_unique_key as dim_value,
        usaspending_permalink::text as dim_label,
        obligations
    from base
    where award_summary_unique_key is not null

    union all

    -- awarding agency (name only)
    select
        fiscal_year,
        fiscal_quarter,
        source_table,
        'awarding_agency' as dim_type,
        awarding_agency_name as dim_value,
        null::text as dim_label,
        obligations
    from base
    where awarding_agency_name is not null

    union all

    -- cfda (number + title)
    select
        fiscal_year,
        fiscal_quarter,
        source_table,
        'cfda' as dim_type,
        cfda_number as dim_value,
        cfda_title as dim_label,
        obligations
    from base
    where cfda_number is not null

    union all

    -- naics (code + description)
    select
        fiscal_year,
        fiscal_quarter,
        source_table,
        'naics' as dim_type,
        naics_code as dim_value,
        naics_description as dim_label,
        obligations
    from base
    where naics_code is not null

    union all

    -- psc (code + description)
    select
        fiscal_year,
        fiscal_quarter,
        source_table,
        'psc' as dim_type,
        product_or_service_code as dim_value,
        product_or_service_code_description as dim_label,
        obligations
    from base
    where product_or_service_code is not null

    union all

    -- recipient (uei + name)
    select
        fiscal_year,
        fiscal_quarter,
        source_table,
        'recipient' as dim_type,
        recipient_uei as dim_value,
        recipient_name as dim_label,
        obligations
    from base
    where recipient_uei is not null
)

select
    fiscal_year,
    fiscal_quarter,
    source_table,
    dim_type,
    dim_value,
    max(dim_label) as dim_label,
    sum(obligations) as obligations
from long
group by 1,2,3,4,5