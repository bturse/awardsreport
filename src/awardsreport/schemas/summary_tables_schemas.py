from pydantic import BaseModel, validator
from datetime import date
from typing import Literal

GroupByCol = Literal[
    "action_date_month",
    "action_date_year",
    "assistance_award_unique_key",
    "assistance_type_code",
    "award_summary_unique_key",
    "awarding_agency_code",
    "awarding_agency_name",
    "cfda_number",
    "cfda_title",
    "contract_award_unique_key",
    "contract_transaction_unique_key",
    "naics_code",
    "naics_description",
    "primary_place_of_performance_state_name",
    "product_or_service_code_description",
    "product_or_service_code",
    "recipient_name",
    "recipient_uei",
]


class GroupBySumFilterLimitQuery(BaseModel):
    gb: list[GroupByCol]
    year: int | None = None
    month: int | None = None
    limit: int | None = None

    @validator("year")
    def check_year_in_2008_cy(cls, v):
        this_year = date.today().year
        if v and (v < 2008 or v > this_year):
            raise ValueError("year must be within 2008 - {this_year}.")
        return v

    @validator("month")
    def check_valid_month(cls, v):
        if v and (v < 1 or v > 12):
            raise ValueError("month must be within 1 - 12.")
        return v


class SummaryRow(BaseModel):
    grouping: list[str]
    obligations: float
