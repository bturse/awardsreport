from awardsreport.models import Transactions as T
from dataclasses import dataclass
from datetime import date
from fastapi import Query
from pydantic import BaseModel, validator
from typing import Literal, Optional, Annotated

gb_values = Literal[
    "atc",
    "awag",
    "awid",
    "cfda",
    "naics",
    "ppopst",
    "ppopct",
    "psc",
    "uei",
    "y",
    "ym",
]

atc_values = Literal["02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]


class GroupByStatementSchema(BaseModel):
    gb: Annotated[list[gb_values], Query(..., description="Group by these columns.")]

    @validator("gb")
    def gb_not_empty(cls, v):
        if len(v) > 0:
            return v
        else:
            raise ValueError("gb must not be an empty list.")


class FilterStatementSchema(BaseModel):
    atc: Annotated[
        Optional[list[Literal[atc_values]]],
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
    ppopct: Annotated[
        Optional[list[str]],
        Query(
            description=T.prime_award_transaction_place_of_performance_county_fips_code.doc,
            example=["01001", "17097"],
        ),
    ] = None
    ppopst: Annotated[
        Optional[list[str]],
        Query(
            description=f"**Primary Place of Performance State Name**. {T.primary_place_of_performance_state_name.doc}",
            example=["FL", "GA"],
        ),
    ] = None
    psc: Annotated[
        Optional[list[str]],
        Query(
            description=f"Product or Service Code. {T.product_or_service_code.doc}",
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


class LimitStatementSchema(BaseModel):
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
