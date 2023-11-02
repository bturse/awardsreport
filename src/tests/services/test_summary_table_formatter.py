from awardsreport.services import summary_table_formatter
from awardsreport.schemas import summary_tables_schemas
from awardsreport.logic import summary_tables
from tests.factories import TransactionsFactory
from sqlalchemy.orm import Session
from awardsreport.database import engine
import pytest


@pytest.fixture
def test_data():
    return [
        TransactionsFactory(
            awarding_agency_name="agency1",
            cfda_title="cfda1",
            generated_pragmatic_obligations=5,
        ),
        TransactionsFactory(
            awarding_agency_name="agency1",
            cfda_title="cfda1",
            generated_pragmatic_obligations=-1,
        ),
        TransactionsFactory(
            awarding_agency_name="agency1",
            cfda_title="cfda2",
            generated_pragmatic_obligations=3,
        ),
        TransactionsFactory(
            awarding_agency_name="agency2",
            cfda_title="cfda2",
            generated_pragmatic_obligations=-5,
        ),
    ]


def test_create_schema_field_dict():
    group_by_statement_schema = summary_tables_schemas.GroupByStatementSchema(
        gb=["atc", "awag"]
    )
    results = summary_table_formatter.create_schema_field_dict(
        group_by_statement_schema
    )
    expected_results = {
        "fields": [
            {"name": "atc", "title": "Assistance Type Code", "type": "string"},
            {"name": "awag", "title": "Awarding Agency Name", "type": "string"},
            {"name": "obligations", "title": "obligations", "type": "number"},
        ]
    }
    assert results == expected_results


def test_create_data_schema_list(db_session: Session, test_data):
    group_by_schema = summary_tables_schemas.GroupByStatementSchema(gb=["awag", "cfda"])
    filter_schema = summary_tables_schemas.FilterStatementSchema()
    limit_schema = summary_tables_schemas.LimitStatementSchema()
    stmt = summary_tables.create_group_by_sum_filter_limit_statement(
        group_by_schema, filter_schema, limit_schema
    )
    with Session(engine) as sess:
        sess.add_all(test_data)
        results = sess.execute(stmt)
    results = summary_table_formatter.create_data_schema_list(group_by_schema, results)
    expected_results = [
        {"awag": "agency1", "cfda": "cfda1", "obligations": 4.0},
        {"awag": "agency1", "cfda": "cfda2", "obligations": 3.0},
        {"awag": "agency2", "cfda": "cfda2", "obligations": -5.0},
    ]
    assert results == expected_results


def test_create_table_schema_response(db_session: Session, test_data):
    group_by_schema = summary_tables_schemas.GroupByStatementSchema(gb=["awag", "cfda"])
    filter_schema = summary_tables_schemas.FilterStatementSchema()
    limit_schema = summary_tables_schemas.LimitStatementSchema()
    stmt = summary_tables.create_group_by_sum_filter_limit_statement(
        group_by_schema, filter_schema, limit_schema
    )
    with Session(engine) as sess:
        sess.add_all(test_data)
        results = sess.execute(stmt)
    results = summary_table_formatter.create_table_schema_response(
        group_by_schema, results
    )
    expected_results = {
        "schema": {
            "fields": [
                {"name": "awag", "title": "Awarding Agency Name", "type": "string"},
                {"name": "cfda", "title": "CFDA Number", "type": "string"},
                {"name": "obligations", "title": "obligations", "type": "number"},
            ]
        },
        "data": [
            {"awag": "agency1", "cfda": "cfda1", "obligations": 4.0},
            {"awag": "agency1", "cfda": "cfda2", "obligations": 3.0},
            {"awag": "agency2", "cfda": "cfda2", "obligations": -5.0},
        ],
    }
    assert results == expected_results
