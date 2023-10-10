from sqlalchemy import select, func, desc, Select, Column
from sqlalchemy.orm import Session
from awardsreport.models import Transactions
from awardsreport.schemas import summary_tables_schemas
import logging.config
from awardsreport import log_config

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")


def str_to_col(
    cols: summary_tables_schemas.GroupByCol | list[summary_tables_schemas.GroupByCol],
) -> list[Column]:
    """Retrieve the specified SQlAlchemy ORM mapped Columns from the transactions table.

    args:
        cols: summary_tables_schemas.TransactionGroupBy |
        list[summary_tables_schemas.TransactionGroupBy] the column(s)
        to retrieve.

    returns list[Column] column ORM objects from transactions table
    """
    if not isinstance(cols, list):
        cols = [cols]
    col_orm_list = []
    for col in cols:
        col_orm_list.append(getattr(Transactions, str(col)))
    return col_orm_list


def groupby_sum_filter_limit(
    session: Session, query: summary_tables_schemas.GroupBySumFilterLimitQuery
) -> Select:
    """Generate SQL statement to find sum of column by grouping.

    args:
        session: Session
        query: summary_tables_schemas.GroupBySumFilterLimitQuery

    returns sqlalchemy.Select
    """
    gb_cols = str_to_col(query.gb)
    stmt = (
        select(
            *gb_cols,
            func.sum(Transactions.generated_pragmatic_obligations).label(
                "sum_spending"
            ),
        )
        .group_by(*gb_cols)
        .order_by(desc("sum_spending").nulls_last())
        .limit(query.limit)
    )
    if query.year:
        stmt = stmt.where(Transactions.action_date_year == query.year)
    if query.month:
        stmt = stmt.where(Transactions.action_date_month == query.month)
    for col in gb_cols:
        stmt = stmt.where(col != None)
    return stmt
