from awardsreport.logic import summary_tables
from awardsreport.main import app
from awardsreport.models import Transactions as T
from awardsreport.schemas import summary_tables_schemas
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import and_, true
from typing import get_args
import pytest

client = TestClient(app)


def test_create_group_by_col_list_one():
    group_by_statement_schema = summary_tables_schemas.GroupByStatementSchema(
        gb=["atc"]
    )
    results = summary_tables.create_group_by_col_list(group_by_statement_schema)
    expected_results = [T.assistance_type_code]
    assert results == expected_results


def test_create_group_by_col_list_each():
    keys = get_args(summary_tables_schemas.gb_values)
    for key in keys:
        group_by_statement_schema = summary_tables_schemas.GroupByStatementSchema(
            gb=[key]
        )
        results = summary_tables.create_group_by_col_list(group_by_statement_schema)
        expected_results = [summary_tables.group_by_key_col.get(key)]
        assert results == expected_results


def test_create_group_by_col_list_all():
    keys = get_args(summary_tables_schemas.gb_values)
    group_by_statement_schema = summary_tables_schemas.GroupByStatementSchema(
        gb=keys  # type:ignore
    )
    expected_results = [summary_tables.group_by_key_col.get(key) for key in keys]
    results = summary_tables.create_group_by_col_list(group_by_statement_schema)
    assert results == expected_results


def test_create_group_by_col_list_invalid():
    with pytest.raises(ValidationError):
        summary_tables_schemas.GroupByStatementSchema(gb=["fake"])  # type: ignore


def test_create_group_by_col_list_gb_none():
    with pytest.raises(ValidationError):
        summary_tables_schemas.GroupByStatementSchema(gb=None)  # type: ignore


def test_create_group_by_col_list_gb_empty():
    with pytest.raises(ValidationError):
        summary_tables_schemas.GroupByStatementSchema(gb=[])  # type: ignore


def test_create_filter_statement_atc_valid():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(atc=["02"])
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(true, T.assistance_type_code.in_(["02"]))
    assert results.compare(expected_results)


def test_create_filter_statement_atc_invalid():
    with pytest.raises(ValidationError):
        summary_tables_schemas.FilterStatementSchema(atc=["fake"])  # type: ignore


def test_create_filter_statement_empty():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema()
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(true)
    assert results.compare(expected_results)


def test_create_filter_statement_awag():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        awag=["070", "069"]
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(true, T.awarding_agency_code.in_(["070", "069"]))
    assert results.compare(expected_results)


def test_create_filter_statement_awid():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        awid=["CONT_123", "ASST_456"]
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(
        true, T.award_summary_unique_key.in_(["CONT_123", "ASST_456"])
    )
    assert results.compare(expected_results)


def test_create_filter_statement_cfda():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        awid=["CONT_123", "ASST_456"]
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(
        true, T.award_summary_unique_key.in_(["CONT_123", "ASST_456"])
    )
    assert results.compare(expected_results)


def test_create_filter_statement_end_date():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        end_date="2023-01-01"
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(true, T.action_date <= "2023-01-01")
    assert results.compare(expected_results)


def test_create_filter_statement_naics():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        naics=["211111", "211112"]
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(true, T.naics_code.in_(["211111", "211112"]))
    assert results.compare(expected_results)


def test_create_filter_statement_ppopct():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        ppopct=["01001"]
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(
        true,
        T.prime_award_transaction_place_of_performance_county_fips_code.in_(["01001"]),
    )
    assert results.compare(expected_results)


def test_create_filter_statement_ppopst():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        ppopst=["FLORIDA", "CALIFORNIA"]
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(
        true, T.primary_place_of_performance_state_name.in_(["FLORIDA", "CALIFORNIA"])
    )
    assert results.compare(expected_results)


def test_create_filter_statement_psc():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        psc=["AA10", "B503", "1005"]
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(
        true, T.product_or_service_code.in_(["AA10", "B503", "1005"])
    )
    assert results.compare(expected_results)


def test_create_filter_statement_start_date():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        start_date="2023-01-01"
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(true, T.action_date >= "2023-01-01")
    assert results.compare(expected_results)


def test_create_filter_statement_uei():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        uei=["abc", "def"]
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(true, T.recipient_uei.in_(["abc", "def"]))
    assert results.compare(expected_results)


def test_create_filter_statement_y():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        y=[2022, 2023]
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(true, T.action_date_year.in_([2022, 2023]))
    assert results.compare(expected_results)


def test_create_filter_statement_ym():
    filter_statement_schema = summary_tables_schemas.FilterStatementSchema(
        ym=["2023-01", "2023-02"]
    )
    results = summary_tables.create_filter_statement(filter_statement_schema)
    expected_results = and_(true, T.action_date_year_month.in_(["2023-01", "2023-02"]))
    assert results.compare(expected_results)
