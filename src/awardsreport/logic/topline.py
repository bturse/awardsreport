from awardsreport.database import Session
from awardsreport.models import ContractTransactions
from sqlalchemy import select, func, desc


def get_agency_obligations(record_limit: int = 3):
    session = Session()
    stmt = (
        select(
            ContractTransactions.awarding_agency_name,
            func.sum(ContractTransactions.federal_action_obligation).label("sum_obl"),
        )
        .group_by(ContractTransactions.awarding_agency_name)
        .order_by(desc("sum_obl"))
        .limit(record_limit)
    )
    results = session.execute(stmt).all()
    ag_ob = [
        {
            "awarding_agency_name": result.awarding_agency_name,
            "sum_obl": result.sum_obl,
        }
        for result in results
    ]
    return ag_ob
