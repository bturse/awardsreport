{% macro fiscal_year(date_expr) -%}
(
    case
        when extract(month from {{ date_expr }}) >= 10
            then extract(year from {{ date_expr }})::int + 1
        else extract(year from {{ date_expr }})::int
    end
)
{%- endmacro %}

{% macro fiscal_quarter(date_expr) -%}
(
    case
        when extract(month from {{ date_expr }}) in (10, 11, 12) then 1
        when extract(month from {{ date_expr }}) in (1, 2, 3) then 2
        when extract(month from {{ date_expr }}) in (4, 5, 6) then 3
    end
)
{%- endmacro %}