from pydantic import BaseModel
from typing import Literal


class AwardsPayloadFilterDateRange(BaseModel):
    start_date: str
    end_date: str


class AwardsPayloadFilterAgencies(BaseModel):
    type: Literal["awarding"] = "awarding"
    tier: Literal["toptier"] = "toptier"
    name: Literal["All"] = "All"


class AwardsPayloadFilters(BaseModel):
    prime_award_types: list[str]
    date_type: Literal["action_date"] = "action_date"
    date_range: AwardsPayloadFilterDateRange
    agencies: list[AwardsPayloadFilterAgencies]


class AwardsPayload(BaseModel):
    columns: list[str]
    filters: AwardsPayloadFilters
    file_format: Literal["csv"] = "csv"
