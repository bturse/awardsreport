from fastapi import APIRouter, Depends, Query

from awardsreport.logic import summary_tables
from awardsreport.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
import logging

logger = logging.getLogger("root")

router = APIRouter(prefix="/summary_tables")


@router.get("/")
async def create_summary_table(
    db: Session = Depends(get_db),
    # need to figure out how to pass list as query param:
    # https://fastapi.tiangolo.com/tutorial/query-params-str-validations/
    gb: Annotated[list[str] | None, Query()] = None,
    sum_col: str | None = Query(None),
    y: int | None = Query(None),
    m: int | None = Query(None),
    limit: int = Query(10),
):
    _gb = summary_tables.str_to_col("assistance_transactions", gb)
    _sum_col = summary_tables.str_to_col("assistance_transactions", sum_col)
    stmt = summary_tables.groupby_sum_filter_limit(
        groupby_cols=_gb, sum_col=_sum_col, year=y, month=m, limit=limit
    )
    logging.info(stmt)
    results = db.execute(stmt).fetchall()
    results_dict = {}
    for result in results:
        results_dict[result[0]] = {result[1:]}
    return results_dict
