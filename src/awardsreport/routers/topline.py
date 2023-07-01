from fastapi import APIRouter
from typing import List

from awardsreport.logic.topline import get_agency_obligations
from awardsreport.schemas.topline import AgencyObligations

router = APIRouter(prefix="/topline", tags=["topline"])


@router.get("/top_agency_obligation", response_model=List[AgencyObligations])
async def list_agency_obligations(record_limit: int = 3):
    return get_agency_obligations(record_limit)
