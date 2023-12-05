from awardsreport import log_config
from awardsreport.models import Transactions as T
from awardsreport.schemas import (
    FilterStatementSchema,
    GroupByStatementSchema,
    LimitStatementSchema,
)
from fastapi import Depends
from sqlalchemy import select, func, desc, Select, and_, true
from sqlalchemy.orm import InstrumentedAttribute
from typing import Any, Annotated
import logging.config

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")


# keys represent filter key passed to summary_tables.
# values represent lambda functions to filter using parameter values.
filter_key_op = {
    "atc": lambda v: T.assistance_type_code.in_(v),
    "awag": lambda v: T.awarding_agency_code.in_(v),
    "awid": lambda v: T.award_summary_unique_key.in_(v),
    "cfda": lambda v: T.cfda_number.in_(v),
    "end_date": lambda v: (T.action_date <= v),
    "naics": lambda v: T.naics_code.in_(v),
    "ppopst": lambda v: T.primary_place_of_performance_state_name.in_(v),
    "ppopct": lambda v: T.prime_award_transaction_place_of_performance_county_fips_code.in_(
        v
    ),
    "psc": lambda v: T.product_or_service_code.in_(v),
    "start_date": lambda v: (T.action_date >= v),
    "uei": lambda v: T.recipient_uei.in_(v),
    "y": lambda v: T.action_date_year.in_(v),
    "ym": lambda v: T.action_date_year_month.in_(v),
}

# keys represent filter key passed to summary_tables.
# values represent lambda functions to filter using parameter values.
group_by_key_col = {
    "atc": T.assistance_type_code,
    "awag": T.awarding_agency_name,
    "awid": T.award_summary_unique_key,
    "cfda": T.cfda_title,
    "naics": T.naics_description,
    "ppopst": T.primary_place_of_performance_state_name,
    "ppopct": T.prime_award_transaction_place_of_performance_county_fips_code,
    "psc": T.product_or_service_code_description,
    "uei": T.recipient_name,
    "y": T.action_date_year,
    "ym": T.action_date_year_month,
}


def create_group_by_col_list(
    schema: GroupByStatementSchema,
) -> list[InstrumentedAttribute]:
    """Generate list of ORM mapped columns to group by.

    params
        schema: summary_tables_schemas.GroupByStatementSchema

    return list[InstrumentedAttribute]
    """
    group_by_col_list = []
    for col in schema.gb:
        if col in group_by_key_col.keys():
            gb_col = group_by_key_col[col]
            group_by_col_list.append(gb_col)

    return group_by_col_list


def create_filter_statement(schema: Annotated[FilterStatementSchema, Depends()]) -> Any:
    """Combine filters using and to create filter statement for SQLAlchemy Select.

    Combines all filters using AND logic.

    params
        schema: Annotated[summary_tables_schemas.FilterStatementSchema, Depends()]

    return Any apply to SQLAlchemy Select to filter results.
    """
    filter_statement_list = []
    for key in schema.__annotations__:
        if key in filter_key_op:
            value = schema[key]
            if value:
                filter_statement = filter_key_op[key](value)
                filter_statement_list.append(filter_statement)
    # filter by sqlalchemy.true to avoid deprecation warning
    return and_(true, *filter_statement_list)


def create_group_by_sum_filter_limit_statement(
    group_by_schema: GroupByStatementSchema,
    filter_schema: FilterStatementSchema,
    limit_schema: LimitStatementSchema,
) -> Select:
    """Create SQLAlchemy Select using provided group by, filter, and limit values.

    Filters are combined using AND logic. group by columns are filtered for not null.

    params
        group_by_schema: summary_tables_schemas.GroupByStatementSchema,
        filter_schema: summary_tables_schemas.FilterStatementSchema,
        limit_schema: summary_tables_schemas.LimitStatementSchema,

    return Select
    """
    filter_statement = create_filter_statement(filter_schema)
    group_by_col_list = create_group_by_col_list(group_by_schema)

    stmt = (
        select(
            *group_by_col_list,
            func.sum(T.generated_pragmatic_obligations).label("sum_spending"),
        )
        .group_by(*group_by_col_list)
        .where(and_(*[col.isnot(None) for col in group_by_col_list]))
        .where(filter_statement)
        .limit(limit_schema.limit)
        .order_by(desc("sum_spending"))
    )
    return stmt
