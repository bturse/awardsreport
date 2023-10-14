import logging.config
from fastapi import APIRouter, Depends, Query
from awardsreport import log_config
from awardsreport.logic import summary_tables
from awardsreport.database import get_db
from awardsreport.schemas import summary_tables_schemas
from sqlalchemy.orm import Session
from typing import Optional

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")

router = APIRouter(prefix="/summary_tables")


def validate_group_by_sum_filter_limit(
    gb: list[summary_tables_schemas.GroupByCol] = Query(
        None,
        description="""group by columns, unique combinations of values in these
        fields will be summed on separate `SummaryRow` objects.""",
    ),
    y: Optional[int] = Query(
        None,
        description="""sum spending on transactions with
    `action_date` in specified year.""",
    ),
    m: Optional[int] = Query(
        None,
        description="""sum spending on transactions with `action_date` in
        specified month.""",
    ),
    limit: int = Query(
        10,
        description="number of groups to return as `SummaryRow` objects.",
    ),
):
    return summary_tables_schemas.GroupBySumFilterLimitQuery(
        gb=gb, year=y, month=m, limit=limit
    )


@router.get("/", response_model=summary_tables_schemas.SummaryTable)
async def create_summary_table(
    db: Session = Depends(get_db),
    query: summary_tables_schemas.GroupBySumFilterLimitQuery = Depends(
        validate_group_by_sum_filter_limit
    ),
) -> summary_tables_schemas.SummaryTable:
    """Generate total spending by specified group by columns and selected filters.

    returns `limit` rows descending by total spending.
    """
    stmt = summary_tables.groupby_sum_filter_limit(db, query=query)
    logger.info(stmt)
    results = db.execute(stmt).fetchall()
    results_list = []
    for result in results:
        summary_row = summary_tables_schemas.SummaryRow(
            grouping=result[0:-1], obligations=(result[-1])  # type: ignore
        )
        results_list.append(summary_row)
    return summary_tables_schemas.SummaryTable(results=results_list)
