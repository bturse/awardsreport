import pytest
from awardsreport.logic import topline
from awardsreport.database import Session

from tests.factories import AssistanceTransactionsFactory


def test_get_award_type_month_total(db_session):
    db_session.add(
        AssistanceTransactionsFactory(
            federal_action_obligation=100,
            action_date="2023-05-01",
            assistance_transaction_unique_key=1,
        )
    )
    db_session.add(
        AssistanceTransactionsFactory(
            federal_action_obligation=100,
            action_date="2023-05-01",
            assistance_transaction_unique_key=2,
        )
    )
    db_session.commit()

    result = topline.get_award_type_month_total(db_session, "assistance", 2023, 5)
    expected_result = 200
    assert result == expected_result
