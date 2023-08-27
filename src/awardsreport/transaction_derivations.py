from sqlalchemy import select, insert, case, Insert, Update, update
from sqlalchemy.orm import Session
from awardsreport.models import (
    AssistanceTransactions,
    ProcurementTransactions,
)
from awardsreport.database import sess
import logging
from typing import Type

logging.basicConfig(
    filename=f"{__name__}.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d  %(message)s",
)

session = sess()


def set_generated_pragmatic_obligations(
    table: Type[AssistanceTransactions] | Type[ProcurementTransactions],
) -> Update:
    if table == AssistanceTransactions:
        if AssistanceTransactions.assistance_type_code in ("07", "08"):
            return update(AssistanceTransactions).values(
                generated_pragmatic_obligations=AssistanceTransactions.original_loan_subsidy_cost
            )
        else:
            return update(AssistanceTransactions).values(
                generated_pragmatic_obligations=AssistanceTransactions.federal_action_obligation
            )
    elif table == ProcurementTransactions:
        return update(ProcurementTransactions).values(
            generated_pragmatic_obligations=ProcurementTransactions.federal_action_obligation
        )
    else:
        raise ValueError(
            "table must be AssistanceTransactions or ProcurementTransactions"
        )


if __name__ == "__main__":
    session.execute(set_generated_pragmatic_obligations(AssistanceTransactions))
    session.execute(set_generated_pragmatic_obligations(ProcurementTransactions))
    session.commit()
