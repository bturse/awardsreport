from fastapi import APIRouter

from awardsreport.seed import awards_13_mo_usas_to_sql

router = APIRouter(prefix="/import", tags=["import"])


@router.get("")
async def awards_13_mo_usas_to_sql(year: int, month: int):
    awards_13_mo_usas_to_sql(year, month)
