from fastapi import APIRouter, Depends, Query
from typing import List

from awardsreport.logic import topline
from awardsreport.schemas.topline import AgencyObligations
from awardsreport.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/topline", tags=["topline"])


@router.get("/award_type_month_total", response_model=int)
async def award_type_month_total(
    db: Session = Depends(get_db),
    award_type: str = Query(...),
    year: int = Query(...),
    month: int = Query(...),
):
    result = topline.get_award_type_month_total(db, award_type, year, month)
    return result
