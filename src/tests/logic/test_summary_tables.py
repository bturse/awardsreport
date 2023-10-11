import pytest
from awardsreport.database import engine
from awardsreport.logic import summary_tables
from awardsreport.main import app
from awardsreport.routers.summary_tables import router
from awardsreport.schemas import summary_tables_schemas
from datetime import date
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy.orm import Session
from tests.factories import TransactionsFactory
from typing import get_args

client = TestClient(app)


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


def test_valid_group_by_col(db_session):
    response = client.get(
        f"{router.prefix}/?gb={get_args(summary_tables_schemas.GroupByCol)[0]}"
    )
    assert response.status_code == 200


def test_invalid_group_by_col(db_session):
    response = client.get(f"{router.prefix}/?gb=invalidgroupbycol")
    assert response.status_code == 422


def test_invalid_year():
    years = [2000, date.today().year + 1]
    for year in years:
        with pytest.raises(ValidationError):
            summary_tables_schemas.GroupBySumFilterLimitQuery(
                gb=get_args(summary_tables_schemas.GroupByCol)[0],
                year=year,
            )


def test_invalid_month():
    months = [0, 13]
    for month in months:
        with pytest.raises(ValidationError):
            summary_tables_schemas.GroupBySumFilterLimitQuery(
                gb=get_args(summary_tables_schemas.GroupByCol)[0],
                month=month,
            )
