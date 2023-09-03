from pydantic import BaseModel
from sqlalchemy.orm import Mapped
from typing import Optional, Any, List
from enum import Enum


class FederalAccountBalance(BaseModel):
    id: int
    federal_account_symbol: str
    fiscal_year: str
    fiscal_period: str
    total_budgetary_resources: int

    class Config:
        orm_mode = True


class GroupbySumFilterLimit(BaseModel):
    pass


class GroupByColsEnum(str, Enum):
    awarding_agency_code = "awarding_agency_code"
    awarding_agency_name = "awarding_agency_name"
    primary_place_of_performance_state_name = "primary_place_of_performance_state_name"
    recipient_name = "recipient_name"
    recipient_uei = "recipient_uei"
    contract_award_unique_key = "contract_award_unique_key"
    naics_code = "naics_code"
    naics_description = "naics_description"
    product_or_service_code = "product_or_service_code"
    product_or_service_code_description = "product_or_service_code_description"
    assistance_award_unique_key = "assistance_award_unique_key"
    award_summary_unique_key = "award_summary_unique_key"
    assistance_type_code = "assistance_type_code"
    cfda_number = "cfda_number"
    cfda_title = "cfda_title"
    action_date_month = "action_date_month"
    action_date_year = "action_date_year"


class GroupBy(BaseModel):
    cols: GroupByColsEnum | List[GroupByColsEnum]
