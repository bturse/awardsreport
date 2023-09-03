from sqlalchemy import select, func, desc, Table, Select, Column
from typing import Optional, Any, Literal
from sqlalchemy.orm import Session, Mapped
from awardsreport.models import AssistanceTransactions, ProcurementTransactions
from awardsreport.database import sess


def str_to_col(
    table: Literal["assistance_transactions"] | Literal["procurement_transactions"],
    cols: list[str] | str,
) -> list[Column]:
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
    else:
        raise ValueError(
            "table must be either 'assistance_transactions' or 'procurement_transactions'"
        )
    if not isinstance(cols, list):
        cols = [cols]
    col_list = []
    for col in cols:
        col_list.append(getattr(_table, col))
    return col_list


def groupby_sum_filter_limit(
    session: Session,
    groupby_cols: list[Column] | Column,
    sum_col: Mapped[Optional[float]] | None = None,
    filters: dict = {},
    limit: int = 10,
) -> Select:
    """Generate SQL statement to find sum of column by grouping.

    args:
        session sqlalchemy.orm.Session
        group_by_cols Mapped[Optional[Any]] | list[Mapped[Optional[Any]]]
            Columns to include in group by statement. May either be a list of
            columns or a single column.
        sum_col: Mapped[Optional[float]] | None column to sum. Defaults to
            generated_pragmatic_obligations on the table of the first element
            from group_by_cols.
        filters: dict keys are string representation of column elements, values
            are values to filter for.
        limit: int the number of results to return sorted by sum(sum_col)
            descending.

    returns sqlalchemy.Select

    raises ValueError if all group_by_cols do not share the same class.


    """
    if not isinstance(groupby_cols, list):
        groupby_cols = [groupby_cols]
    table: Table = groupby_cols[0].class_  # type: ignore (pylance does not recognice .class_)
    for col in groupby_cols:
        if col.class_ != table:  # type: ignore
            raise ValueError(
                "All columns passed to group_by must share the same class."
            )
    if sum_col is None:
        sum_col = table.generated_pragmatic_obligations  # type: ignore
    stmt = (
        select(*groupby_cols, func.sum(sum_col).label("sum"))
        .filter_by(**filters)
        .group_by(*groupby_cols)
        .order_by(desc("sum"))
        .limit(limit)
    )
    return stmt


if __name__ == "__main__":
    c = str_to_col("procurement_transactions", "awarding_agency_name")
    session = sess()
    stmt = groupby_sum_filter_limit(session, groupby_cols=c)
    print(stmt)
