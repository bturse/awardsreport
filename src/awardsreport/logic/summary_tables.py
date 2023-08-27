from sqlalchemy import Column, select, func, desc, Float
from typing import Optional
from sqlalchemy.orm import Session
from awardsreport.models import AssistanceTransactions
from pydantic import BaseModel
from sqlalchemy.orm import Mapped

sess = Session()


def groupby_sum(
    #    sess: Session,
    group_by_cols: Mapped[Optional[str]] | list[Mapped[Optional[str]]],
    sum_col: Mapped[Optional[float]],
):
    if not isinstance(group_by_cols, list):
        group_by_cols = [group_by_cols]
    stmt = (
        select(*group_by_cols, func.sum(sum_col).label("ct"))
        .group_by(*group_by_cols)
        .order_by(desc("ct"))
    )
    return stmt


if __name__ == "__main__":
    print(type(AssistanceTransactions.awarding_agency_name))
    stmt = groupby_sum(
        group_by_cols=AssistanceTransactions.awarding_agency_name,
        sum_col=AssistanceTransactions.generated_pragmatic_obligations,
    )
    print(stmt)
