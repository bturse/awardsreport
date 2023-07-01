from pydantic import BaseModel


class AgencyObligations(BaseModel):
    awarding_agency_name: str
    sum_obl: float
