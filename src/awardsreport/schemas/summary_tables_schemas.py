from awardsreport.models import Transactions as T
from datetime import date
from fastapi import Query, Depends
from pydantic import BaseModel, validator, Field
from sqlalchemy import and_, BinaryExpression
from typing import get_args, Literal, Optional, TypedDict, cast, List, Annotated
from dataclasses import dataclass


@dataclass
class GroupByStatementSchema:
    gb: list[
        Literal[
            "atc",
            "awag",
            "awid",
            "cfda",
            "naics",
            "ppopst",
            "psc",
            "uei",
            "y",
            "ym",
        ]
    ] = Query(..., description="Group by these columns.")


@dataclass
class FilterStatementSchema:
    atc: Annotated[
        Optional[
            list[Literal["02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]]
        ],
        Query(
            description=T.assistance_type_code.doc,
            example=["02", "03"],
        ),
    ] = None
    awag: Annotated[
        Optional[list[str]],
        Query(
            description=T.awarding_agency_code.doc,
            example=["069", "077"],
        ),
    ] = None
    awid: Annotated[
        Optional[list[str]],
        Query(
            description=T.award_summary_unique_key.doc,
            example=["CONT_IDV_36F79718D0583_3600", "CONT_IDV_36C10X23D0035_3600"],
        ),
    ] = None
    cfda: Annotated[
        Optional[list[str]],
        Query(
            description=T.cfda_number.doc,
            example=["19.040", "59.008"],
        ),
    ] = None
    end_date: Annotated[
        Optional[str],
        Query(
            description="""('YYYY-MM-DD') Filter for transactions with action
            date on or before this date.""",
            example=str(date.today()),
        ),
    ] = None
    naics: Annotated[
        Optional[list[str]],
        Query(
            description=T.naics_code.doc,
            example=["111110", "111120"],
        ),
    ] = None
    ppopst: Annotated[
        Optional[list[str]],
        Query(
            description=T.primary_place_of_performance_state_name.doc,
            example=["FL", "GA"],
        ),
    ] = None
    psc: Annotated[
        Optional[list[str]],
        Query(
            description=T.product_or_service_code.doc,
            example=["1005", "1010"],
        ),
    ] = None
    start_date: Annotated[
        Optional[str],
        Query(
            description="""('YYYY-MM-DD') Filter for transactions with action date
        on or after this date.""",
            example="2023-01-31",
        ),
    ] = None
    uei: Annotated[
        Optional[list[str]],
        Query(
            description=T.recipient_uei.doc,
            example=["fakeuei1", "fakeuei2"],
        ),
    ] = None
    y: Annotated[
        Optional[list[int]],
        Query(
            description=T.action_date_year.doc,
            example=[2022, 2023],
        ),
    ] = None
    ym: Annotated[
        Optional[list[str]],
        Query(
            description=T.action_date_year_month.doc,
            example=["2023-01", "2023-02"],
        ),
    ] = None

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class LimitStatementSchema:
    limit: Annotated[
        Optional[int],
        Query(
            description="Limit number of records returned.",
            example=10,
        ),
    ] = 10


class SummaryRow(BaseModel):
    grouping: list[str]
    obligations: float


class SummaryTable(BaseModel):
    results: list[SummaryRow]
