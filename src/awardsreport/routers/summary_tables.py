from awardsreport import log_config
from awardsreport.database import get_db
from awardsreport.logic import summary_tables
from awardsreport.schemas import summary_tables_schemas
from awardsreport.services import summary_table_formatter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
import logging.config

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")

router = APIRouter(prefix="/summary_tables")


@router.get(
    "/",
    response_model=summary_tables_schemas.TableSchema,
    response_model_exclude_none=True,
)
async def create_summary_table(
    db: Annotated[Session, Depends(get_db)],
    group_by_schema: Annotated[
        summary_tables_schemas.GroupByStatementSchema, Depends()
    ],
    filter_schema: Annotated[summary_tables_schemas.FilterStatementSchema, Depends()],
    limit_schema: Annotated[summary_tables_schemas.LimitStatementSchema, Depends()],
):
    """Generate total spending by specified group by columns and selected filters.

    returns `limit` rows descending by total spending.
    """
    stmt = summary_tables.create_group_by_sum_filter_limit_statement(
        group_by_schema, filter_schema, limit_schema
    )
    results = db.execute(stmt)
    return summary_table_formatter.create_table_schema_response(
        group_by_schema, results
    )
