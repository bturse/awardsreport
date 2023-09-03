from fastapi import APIRouter, Depends, Query

from awardsreport.logic import summary_tables
from awardsreport.schemas.summary_tables import GroupBy
from awardsreport.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/summary_table", tags=["summary_table"])
