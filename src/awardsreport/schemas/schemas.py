from pydantic import BaseModel


class FederalAccountBalance(BaseModel):
    id: int
    federal_account_symbol: str
    fiscal_year: str
    fiscal_period: str
    total_budgetary_resources: int

    class Config:
        orm_mode = True
