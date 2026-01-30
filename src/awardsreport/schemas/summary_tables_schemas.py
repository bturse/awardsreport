from awardsreport.models import Transactions as T
from dataclasses import dataclass
from datetime import date
from fastapi import Query
from pydantic import BaseModel, validator, Field, create_model
from typing import Literal, Optional, Annotated, Union

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
        ),
    ] = None
    awag: Annotated[
        Optional[list[str]],
        Query(
            description=T.awarding_agency_code.doc,
        ),
    ] = None
    awid: Annotated[
        Optional[list[str]],
        Query(
            description=T.award_summary_unique_key.doc,
        ),
    ] = None
    cfda: Annotated[
        Optional[list[str]],
        Query(
            description=T.cfda_number.doc,
        ),
    ] = None
    end_date: Annotated[
        Optional[str],
        Query(
            description="""('YYYY-MM-DD') Filter for transactions with action
            date on or before this date.""",
        ),
    ] = None
    naics: Annotated[
        Optional[list[str]],
        Query(
            description=T.naics_code.doc,
        ),
    ] = None
    ppopct: Annotated[
        Optional[list[str]],
        Query(
            description=T.prime_award_transaction_place_of_performance_county_fips_code.doc,
        ),
    ] = None
    ppopst: Annotated[
        Optional[list[str]],
        Query(
            description=f"**Primary Place of Performance State Name**. {T.primary_place_of_performance_state_name.doc}",
        ),
    ] = None
    psc: Annotated[
        Optional[list[str]],
        Query(
            description=f"Product or Service Code. {T.product_or_service_code.doc}",
        ),
    ] = None
    start_date: Annotated[
        Optional[str],
        Query(
            description="""('YYYY-MM-DD') Filter for transactions with action date
        on or after this date.""",
        ),
    ] = None
    uei: Annotated[
        Optional[list[str]],
        Query(
            description=T.recipient_uei.doc,
        ),
    ] = None
    y: Annotated[
        Optional[list[int]],
        Query(
            description=T.action_date_year.doc,
        ),
    ] = None
    ym: Annotated[
        Optional[list[str]],
        Query(
            description=T.action_date_year_month.doc,
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


class TableSchemaField(BaseModel):
    name: Literal[gb_values, Literal["obligations"]]
    title: str
    type: str


class TableSchemaFields(BaseModel):
    fields: list[TableSchemaField]


class TableSchemaData(BaseModel):
    atc: Annotated[
        Optional[str],
        Field(
            title="Assistance Type Code",
            description=T.assistance_type_code.doc,
            response_type="string",
        ),
    ] = None
    awag: Annotated[
        Optional[str],
        Field(
            title="Awarding Agency Name",
            description=T.awarding_agency_name.doc,
            response_type="string",
        ),
    ] = None
    awid: Annotated[
        Optional[str],
        Field(
            title="award_summary_unique_key",
            description=T.award_summary_unique_key.doc,
            response_type="string",
        ),
    ] = None
    cfda: Annotated[
        Optional[str],
        Field(
            title="CFDA Number",
            description=T.cfda_number.doc,
            response_type="string",
        ),
    ] = None
    naics: Annotated[
        Optional[str],
        Field(
            title="NAICS Code",
            description=T.naics_code.doc,
            response_type="string",
        ),
    ] = None
    ppopct: Annotated[
        Optional[str],
        Field(
            title="PPoP County FIPS",
            description=T.prime_award_transaction_place_of_performance_county_fips_code.doc,
            response_type="string",
        ),
    ] = None
    ppopst: Annotated[
        Optional[str],
        Field(
            title="PPoP State Name",
            description=T.primary_place_of_performance_state_name.doc,
            response_type="string",
        ),
    ] = None
    psc: Annotated[
        Optional[str],
        Field(
            title="Product or Service Code",
            description=T.product_or_service_code.doc,
            response_type="string",
        ),
    ] = None
    uei: Annotated[
        Optional[str],
        Field(
            title="Recipient UEI",
            description=T.recipient_uei.doc,
            response_type="string",
        ),
    ] = None
    y: Annotated[
        Optional[int],
        Field(
            title="Action Date Year",
            description=T.action_date_year.doc,
            response_type="number",
        ),
    ] = None
    ym: Annotated[
        Optional[str],
        Field(
            title="Action Date Year Month",
            description=T.action_date_year_month.doc,
            response_type="string",
        ),
    ] = None
    obligations: Annotated[
        float,
        Field(
            title="Total Spending",
            description="Total spending by grouped columns",
            response_type="number",
        ),
    ]


class TableSchema(BaseModel):
    schema_: TableSchemaFields = Field(..., alias="schema")
    data: list[TableSchemaData]
