import pytest
from awardsreport.logic import topline
from sqlalchemy.orm import Session

from tests.factories import AssistanceTransactionsFactory


def test_get_award_type_month_total(db_session: Session):
    db_session.add_all(
        [
            AssistanceTransactionsFactory(
                federal_action_obligation=1, action_date="2023-05-01"
            ),
            AssistanceTransactionsFactory(
                federal_action_obligation=1, action_date="2023-05-31"
            ),
            AssistanceTransactionsFactory(
                federal_action_obligation=-1, action_date="2023-05-01"
            ),
            AssistanceTransactionsFactory(
                federal_action_obligation=1, action_date="2023-06-01"
            ),
            AssistanceTransactionsFactory(
                federal_action_obligation=1, action_date="2022-05-01"
            ),
        ]
    )
    db_session.commit()

    result = topline.get_award_type_month_total(db_session, "assistance", 2023, 5)
    expected_result = 1
    assert result == expected_result
