from sqlalchemy import select, func, desc, Table, Select, Column
from typing import Optional, Any, Literal
from sqlalchemy.orm import Session, Mapped
from awardsreport.models import (
    AssistanceTransactions,
    ProcurementTransactions,
    Transactions,
)
from awardsreport.database import sess, Base
import logging.config
from awardsreport import log_config

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")


def str_to_col(
    table: Literal[
        "assistance_transactions", "procurement_transactions", "transactions"
    ] = "transactions",
    cols: list[str] | str | None = None,
) -> list[Column] | None:
    """Retrieve the specified SQlAlchemy Columns from the specified table.

    args:
        table: Literal["assistance_transactions"] |
            Literal["procurement_transactions"] the table from which to retrieve.
        cols: list[str] | str the columns to retrieve

    returns list[Column]

    raises ValueError table must be either 'assistance_transactions' or 'procurement_transactions'
    """
    if table == "assistance_transactions":
        _table = AssistanceTransactions
    elif table == "procurement_transactions":
        _table = ProcurementTransactions
    elif table == "transactions":
        _table = Transactions
    else:
        raise ValueError(
            "table must be 'transactions', 'assistance_transactions' or 'procurement_transactions'"
        )
    if cols is None:
        return None
    if not isinstance(cols, list):
        cols = [cols]
    col_list = []
    for col in cols:
        col_list.append(getattr(_table, col))
    return col_list


def groupby_sum_filter_limit(
    session: Session,
    groupby_cols: list[Column] | Column | None,
    sum_col: list[Column[float]] | Column[float] | None = None,
    year: int | None = None,
    month: int | None = None,
    limit: int = 10,
) -> Select:
    """Generate SQL statement to find sum of column by grouping.

    args:
        group_by_cols Mapped[Optional[Any]] | list[Mapped[Optional[Any]]]
            Columns to include in group by statement. May either be a list of
            columns or a single column.
        sum_col: Mapped[Optional[float]] | None column to sum. Defaults to
            generated_pragmatic_obligations on the table of the first element
            from group_by_cols.
        year: int | None filter for transactions in this specified calendar year.
        month: int | None filter for transactions in this specified calendar month.
        limit: int the number of results to return sorted by sum(sum_col)
            descending.

    returns sqlalchemy.Select

    raises ValueError if all group_by_cols do not share the same class.
    """
    if groupby_cols is None:
        raise ValueError("group_by cols must not be None.")
    if not isinstance(groupby_cols, list):
        groupby_cols = [groupby_cols]
    table: AssistanceTransactions | ProcurementTransactions = groupby_cols[0].class_
    for col in groupby_cols:
        if col.class_ != table:
            raise ValueError(
                "All columns passed to group_by must share the same class."
            )

    if sum_col is None:
        sum_col = table.generated_pragmatic_obligations  # type: ignore
    stmt = (
        select(*groupby_cols, func.sum(sum_col).label("sum"))
        .group_by(*groupby_cols)
        .order_by(desc("sum").nulls_last())
        .limit(limit)
    )
    if year:
        stmt = stmt.where(table.action_date_year == year)  # type: ignore
    if month:
        stmt = stmt.where(table.action_date_month == month)  # type: ignore
    for col in groupby_cols:
        stmt = stmt.where(col != None)  # type: ignore
    return stmt
