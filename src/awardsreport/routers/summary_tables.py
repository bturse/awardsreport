from awardsreport import log_config
from awardsreport.database import get_db
from awardsreport.logic import summary_tables
from awardsreport.schemas import summary_tables_schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
import logging.config

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")

router = APIRouter(prefix="/summary_tables")


@router.get("/", response_model=summary_tables_schemas.SummaryTable)
async def create_summary_table(
    db: Annotated[Session, Depends(get_db)],
    group_by_schema: Annotated[
        summary_tables_schemas.GroupByStatementSchema, Depends()
    ],
    filter_schema: Annotated[summary_tables_schemas.FilterStatementSchema, Depends()],
    limit_schema: Annotated[summary_tables_schemas.LimitStatementSchema, Depends()],
) -> summary_tables_schemas.SummaryTable:
    """Generate total spending by specified group by columns and selected filters.

    returns `limit` rows descending by total spending.
    """
    stmt = summary_tables.create_group_by_sum_filter_limit_statement(
        group_by_schema, filter_schema, limit_schema
    )
    results = db.execute(stmt).fetchall()
    results_list = []
    for result in results:
        summary_row = summary_tables_schemas.SummaryRow(
            grouping=result[0:-1], obligations=(result[-1])  # type: ignore
        )
        results_list.append(summary_row)

    return summary_tables_schemas.SummaryTable(results=results_list)
