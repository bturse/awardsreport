import pytest
from awardsreport.logic import summary_tables
from awardsreport.database import engine
from awardsreport.models import Transactions
from awardsreport.schemas import summary_tables_schemas
from sqlalchemy.orm import Session

from tests.factories import TransactionsFactory


@pytest.fixture
def test_groupby_multi_data() -> list[TransactionsFactory]:
    return [
        TransactionsFactory(
            generated_pragmatic_obligations=1,
            cfda_number="00.000",
            awarding_agency_name="awag1",
        ),
        TransactionsFactory(
            generated_pragmatic_obligations=1.5,
            cfda_number="00.000",
            awarding_agency_name="awag1",
        ),
        TransactionsFactory(
            generated_pragmatic_obligations=3,
            cfda_number="00.001",
            awarding_agency_name="awag2",
        ),
    ]


def test_groupby_multi(
    db_session: Session,
    test_groupby_multi_data: list[TransactionsFactory],
):
    db_session.bind = engine
    db_session.add_all(test_groupby_multi_data)
    db_session.commit()
    query = summary_tables_schemas.GroupBySumFilterLimitQuery(
        gb=["cfda_number", "awarding_agency_name"]
    )
    stmt = summary_tables.groupby_sum_filter_limit(db_session, query)
    with Session(engine) as sess:
        result = sess.execute(stmt).fetchall()
    expected_result = [
        ("00.001", "awag2", 3),
        ("00.000", "awag1", 2.5),
    ]
    assert result == expected_result
