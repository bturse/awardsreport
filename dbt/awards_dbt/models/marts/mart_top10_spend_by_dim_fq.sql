with ranked as (

    select
        fiscal_year,
        fiscal_quarter,
        source_table,
        dim_type,
        dim_value,
        dim_label,
        obligations,

        row_number() over (
            partition by
                fiscal_year,
                fiscal_quarter,
                source_table,
                dim_type
            order by obligations desc
        ) as rank

    from {{ ref('int_spend_by_dim_fq') }}

)

select *
from ranked
where rank <= 10