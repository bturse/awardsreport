from fastapi import APIRouter, Depends, Query
from awardsreport.logic import summary_tables
from awardsreport.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
import logging.config
from awardsreport import log_config
from awardsreport.schemas import summary_tables_schemas

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")

router = APIRouter(prefix="/summary_tables")


@router.get("/")
async def create_summary_table(
    db: Session = Depends(get_db),
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
    logger.info(stmt)
    results = db.execute(stmt).fetchall()
    results_list = []
    for result in results:
        summary_row = summary_tables_schemas.SummaryRow(
            grouping=result[0:-1], obligations=(result[-1])
        )
        results_list.append(summary_row)
    return results_list
