import logging.config
from fastapi import APIRouter, Depends, Query
from awardsreport import log_config
from awardsreport.logic import summary_tables
from awardsreport.database import get_db
from awardsreport.schemas import summary_tables_schemas
from sqlalchemy.orm import Session

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")

router = APIRouter(prefix="/summary_tables")


@router.get("/")
async def create_summary_table(
    db: Session = Depends(get_db),
    gb: list[summary_tables_schemas.GroupByCol] = Query(None),
    y: int | None = Query(None),
    m: int | None = Query(None),
    limit: int = Query(10),
) -> list[summary_tables_schemas.SummaryRow]:
    validated_query = summary_tables_schemas.GroupBySumFilterLimitQuery(
        gb=gb, year=y, month=m, limit=limit
    )
    stmt = summary_tables.groupby_sum_filter_limit(db, query=validated_query)
    logger.info(stmt)
    results = db.execute(stmt).fetchall()
    results_list = []
    for result in results:
        summary_row = summary_tables_schemas.SummaryRow(
            grouping=result[0:-1], obligations=(result[-1])  # type: ignore
        )
        results_list.append(summary_row)
    return results_list
