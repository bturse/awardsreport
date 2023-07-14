import pytest
from awardsreport.logic import topline
from sqlalchemy.orm import Session

from tests.factories import (
    AssistanceTransactionsFactory,
    ProcurementTransactionsFactory,
)


@pytest.fixture
def test_data():
    return [
        AssistanceTransactionsFactory(
            federal_action_obligation=2,
            action_date="2023-05-01",
            assistance_type_code="01",
        ),
        AssistanceTransactionsFactory(
            federal_action_obligation=-1,
            action_date="2023-05-01",
            assistance_type_code="01",
        ),
        AssistanceTransactionsFactory(
            federal_action_obligation=1,
            action_date="2023-06-01",
            assistance_type_code="01",
        ),
        AssistanceTransactionsFactory(
            federal_action_obligation=1,
            action_date="2022-05-01",
            assistance_type_code="01",
        ),
        AssistanceTransactionsFactory(
            federal_action_obligation=2,
            original_loan_subsidy_cost=3,
            action_date="2023-05-01",
            assistance_type_code="07",
        ),
        ProcurementTransactionsFactory(
            federal_action_obligation=100, action_date="2023-05-01"
        ),
        ProcurementTransactionsFactory(
            federal_action_obligation=-50, action_date="2023-05-01"
        ),
        ProcurementTransactionsFactory(
            federal_action_obligation=100, action_date="2023-06-01"
        ),
    ]


def test_get_award_type_month_total(db_session: Session, test_data: list):
    db_session.add_all(test_data)
    db_session.commit()

    result = topline.get_award_type_month_total(db_session, "assistance", 2023, 5)
    expected_result = 1
    assert result == expected_result

    result = topline.get_award_type_month_total(db_session, "loan", 2023, 5)
    expected_result = 3
    assert result == expected_result

    result = topline.get_award_type_month_total(db_session, "procurement", 2023, 5)
    expected_result = 50
    assert result == expected_result


def test_get_month_totals_award_type_2cat(db_session: Session, test_data: list):
    db_session.add_all(test_data)
    db_session.commit()
    result = topline.get_month_totals_award_type_2cat(db_session, 2023, 5)
    expected_result = {
        "year": 2023,
        "month": 5,
        "total": 54,
        "award_type_totals": {"assistance": 4, "procurement": 50},
    }
    assert result == expected_result
