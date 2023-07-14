from fastapi import APIRouter, Depends, Query

from awardsreport.logic import topline
from awardsreport.schemas.topline import MonthTotalsAwardType2Cat
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


@router.get("/month_totals_award_type_2cat", response_model=MonthTotalsAwardType2Cat)
async def month_totals_award_type_2cat(
    db: Session = Depends(get_db), year: int = Query(...), month: int = Query(...)
):
    result = topline.get_month_totals_award_type_2cat(db, year, month)
    return result
