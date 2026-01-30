from sqlalchemy import select, insert, case, Insert, Update, update, func
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
from awardsreport.models import (
    AssistanceTransactions,
    ProcurementTransactions,
)
from awardsreport.database import sess
from typing import Type

import logging.config
from awardsreport import log_config

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")

from sqlalchemy import update, case, func, Update
from typing import Type
from awardsreport.models import (
    AssistanceTransactions,
    ProcurementTransactions,
)


def set_generated_pragmatic_obligations(
    table: Type[AssistanceTransactions] | Type[ProcurementTransactions],
) -> Update:
    """Set generated_pragmatic_obligations on AssistanceTransactions and
    ProcurementTransactions.

    For AssistanceTransactions:
      - If assistance_type_code indicates a loan ('07' or '08'), use
        original_loan_subsidy_cost.
      - Otherwise, use federal_action_obligation.
      - In all cases, COALESCE to 0.0 to guarantee a non-null value.

    For ProcurementTransactions:
      - Use federal_action_obligation, COALESCE'd to 0.0.

    args
        table: Type[AssistanceTransactions] | Type[ProcurementTransactions]
            The table to update.

    raises
        ValueError if table is not AssistanceTransactions or ProcurementTransactions.

    return
        sqlalchemy.Update to be executed to perform the derivation.
    """
    if table == AssistanceTransactions:
        return update(AssistanceTransactions).values(
            generated_pragmatic_obligations=case(
                (
                    AssistanceTransactions.assistance_type_code.in_(("07", "08")),
                    func.coalesce(
                        AssistanceTransactions.original_loan_subsidy_cost,
                        AssistanceTransactions.federal_action_obligation,
                        0.0,
                    ),
                ),
                else_=func.coalesce(
                    AssistanceTransactions.federal_action_obligation,
                    0.0,
                ),
            )
        )

    elif table == ProcurementTransactions:
        return update(ProcurementTransactions).values(
            generated_pragmatic_obligations=func.coalesce(
                ProcurementTransactions.federal_action_obligation,
                0.0,
            )
        )

    else:
        raise ValueError(
            "table must be AssistanceTransactions or ProcurementTransactions"
        )


def set_action_date_year_month(
    table: Type[AssistanceTransactions] | Type[ProcurementTransactions],
) -> Update:
    """Set action_date_year and action_date_month on AssistanceTransactions and
    ProcurementTransactions.

    Derives using the year and month from table.action_date.

    args
        table: Type[AssistanceTransactions] | Type[ProcurementTransactions] the
            table to set action_date_year and action_date_month.
    raises
        ValueError if table not AssistanceTransactions or ProcurementTransactions

    return sqlalchemy.Update to be executed to perform derivations.
    """
    return update(table).values(
        dict(
            action_date_year=extract("year", table.action_date),
            action_date_year_month=func.to_char(table.action_date, "YYYY-MM"),
        )
    )


def set_award_summary_unique_key(
    table: Type[AssistanceTransactions] | Type[ProcurementTransactions],
) -> Update:
    """Set award_summary_unique_key on AssistanceTransactions and
    ProcurementTransactions.

    Derives using AssistanceTransactions.assistance_award_unique_key or
    ProcurementTransactions.contract_award_unique_key

    args
        table: Type[AssistanceTransactions] | Type[ProcurementTransactions] the
            table to set award_summary_unique_key.
    raises
        ValueError if table not AssistanceTransactions or ProcurementTransactions

    return sqlalchemy.Update to be executed to perform derivations.
    """
    if table == AssistanceTransactions:
        return update(AssistanceTransactions).values(
            award_summary_unique_key=AssistanceTransactions.assistance_award_unique_key
        )
    elif table == ProcurementTransactions:
        return update(ProcurementTransactions).values(
            award_summary_unique_key=ProcurementTransactions.contract_award_unique_key
        )
    else:
        raise ValueError(
            "table must be AssistanceTransactions or ProcurementTransactions"
        )


if __name__ == "__main__":
    session = sess()
    with session.begin():
        # generated_pragmatic_obligations exists in assistance_transactions
        # source file.

        session.execute(set_generated_pragmatic_obligations(ProcurementTransactions))
        session.execute(set_generated_pragmatic_obligations(AssistanceTransactions))

        session.execute(set_action_date_year_month(AssistanceTransactions))
        session.execute(set_action_date_year_month(ProcurementTransactions))

        session.execute(set_award_summary_unique_key(AssistanceTransactions))
        session.execute(set_award_summary_unique_key(ProcurementTransactions))
