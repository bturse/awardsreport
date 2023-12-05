from awardsreport.models import Transactions as T
from awardsreport.schemas import common
from pydantic import BaseModel, Field
from typing import Literal, Optional, Annotated


class TableSchemaField(BaseModel):
    name: Literal[common.gb_values, Literal["obligations"]]
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
