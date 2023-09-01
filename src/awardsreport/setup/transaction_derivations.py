from sqlalchemy import select, insert, case, Insert, Update, update, func
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
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
        return update(AssistanceTransactions).values(
            generated_pragmatic_obligations=case(
                (
                    AssistanceTransactions.assistance_type_code.in_(("07", "08")),
                    AssistanceTransactions.original_loan_subsidy_cost,
                ),
                else_=AssistanceTransactions.federal_action_obligation,
            )
        )
    elif table == ProcurementTransactions:
        return update(ProcurementTransactions).values(
            generated_pragmatic_obligations=ProcurementTransactions.federal_action_obligation
        )
    else:
        raise ValueError(
            "table must be AssistanceTransactions or ProcurementTransactions"
        )


def set_action_date_year_month(
    table: Type[AssistanceTransactions] | Type[ProcurementTransactions],
) -> Update:
    return update(table).values(
        dict(
            action_date_year=extract("year", table.action_date),
            action_date_month=extract("month", table.action_date),
        )
    )


if __name__ == "__main__":
    session.execute(set_generated_pragmatic_obligations(AssistanceTransactions))
    session.execute(set_generated_pragmatic_obligations(ProcurementTransactions))
    session.execute(set_action_date_year_month(AssistanceTransactions))
    session.execute(set_action_date_year_month(ProcurementTransactions))
    session.commit()
    session.close()
