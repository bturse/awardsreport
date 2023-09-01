from sqlalchemy import select, func, desc, Table
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped

sess = Session()


def groupby_sum(
    sess: Session,
    group_by_cols: Mapped[Optional[str]] | list[Mapped[Optional[str]]],
    sum_col: Mapped[Optional[float]],
    limit: int = 10,
):
    if not isinstance(group_by_cols, list):
        group_by_cols = [group_by_cols]
    table: Table = group_by_cols[0].class_  # type: ignore (pylance does not recognice .class_)
    stmt = (
        select(*group_by_cols, func.sum(sum_col).label("ct"))
        .group_by(*group_by_cols)
        .order_by(desc("ct"))
        .limit(limit)
        .where()
    )
    return stmt
