import pytest
from awardsreport.setup import seed_helpers
from awardsreport.models import (
    Transactions,
    AssistanceTransactions,
    ProcurementTransactions,
)
from datetime import datetime


def test_get_raw_columns_invalid_table():
    with pytest.raises(ValueError):
        seed_helpers.get_raw_columns(Transactions)  # type: ignore


def test_get_raw_columns_assistance():
    results = seed_helpers.get_raw_columns(AssistanceTransactions)
    # expected_results will beed to be manually updated if new raw columns are added
    expected_results = [
        "action_date",
        "assistance_award_unique_key",
        "assistance_transaction_unique_key",
        "assistance_type_code",
        "assistance_type_description",
        "awarding_agency_code",
        "awarding_agency_name",
        "awarding_office_code",
        "awarding_office_name",
        "awarding_sub_agency_name",
        "business_types_code",
        "business_types_description",
        "cfda_number",
        "cfda_title",
        "federal_action_obligation",
        "funding_agency_code",
        "funding_agency_name",
        "funding_office_code",
        "funding_office_name",
        "funding_opportunity_number",
        "funding_sub_agency_code",
        "funding_sub_agency_name",
        "initial_report_date",
        "last_modified_date",
        "original_loan_subsidy_cost",
        "period_of_performance_current_end_date",
        "period_of_performance_start_date",
        "primary_place_of_performance_city_name",
        "primary_place_of_performance_code",
        "primary_place_of_performance_country_code",
        "primary_place_of_performance_country_name",
        "primary_place_of_performance_county_name",
        "primary_place_of_performance_foreign_location",
        "primary_place_of_performance_scope",
        "primary_place_of_performance_state_name",
        "primary_place_of_performance_zip_4",
        "prime_award_base_transaction_description",
        "prime_award_transaction_place_of_performance_cd_current",
        "prime_award_transaction_place_of_performance_cd_original",
        "prime_award_transaction_place_of_performance_county_fips_code",
        "prime_award_transaction_place_of_performance_state_fips_code",
        "prime_award_transaction_recipient_cd_current",
        "prime_award_transaction_recipient_cd_original",
        "prime_award_transaction_recipient_county_fips_code",
        "prime_award_transaction_recipient_state_fips_code",
        "recipient_address_line_1",
        "recipient_address_line_2",
        "recipient_city_code",
        "recipient_city_name",
        "recipient_country_code",
        "recipient_country_name",
        "recipient_county_name",
        "recipient_foreign_city_name",
        "recipient_foreign_postal_code",
        "recipient_foreign_province_name",
        "recipient_name",
        "recipient_name_raw",
        "recipient_parent_name",
        "recipient_parent_name_raw",
        "recipient_parent_uei",
        "recipient_state_code",
        "recipient_state_name",
        "recipient_uei",
        "recipient_zip_code",
        "recipient_zip_last_4_code",
        "transaction_description",
        "usaspending_permalink",
    ]
    assert results == expected_results


def test_get_raw_columns_procurement():
    results = seed_helpers.get_raw_columns(ProcurementTransactions)
    expected_results = [
        "action_date",
        "awarding_agency_code",
        "awarding_agency_name",
        "awarding_office_code",
        "awarding_office_name",
        "awarding_sub_agency_name",
        "city_local_government",
        "contract_award_unique_key",
        "contract_transaction_unique_key",
        "county_local_government",
        "domestic_or_foreign_entity",
        "domestic_or_foreign_entity_code",
        "federal_action_obligation",
        "funding_agency_code",
        "funding_agency_name",
        "funding_office_code",
        "funding_office_name",
        "funding_sub_agency_code",
        "funding_sub_agency_name",
        "initial_report_date",
        "inter_municipal_local_government",
        "last_modified_date",
        "local_government_owned",
        "municipality_local_government",
        "naics_code",
        "naics_description",
        "period_of_performance_current_end_date",
        "period_of_performance_potential_end_date",
        "period_of_performance_start_date",
        "primary_place_of_performance_city_name",
        "primary_place_of_performance_country_code",
        "primary_place_of_performance_country_name",
        "primary_place_of_performance_county_name",
        "primary_place_of_performance_state_code",
        "primary_place_of_performance_state_name",
        "primary_place_of_performance_zip_4",
        "prime_award_base_transaction_description",
        "prime_award_transaction_place_of_performance_cd_current",
        "prime_award_transaction_place_of_performance_cd_original",
        "prime_award_transaction_place_of_performance_county_fips_code",
        "prime_award_transaction_place_of_performance_state_fips_code",
        "prime_award_transaction_recipient_cd_current",
        "prime_award_transaction_recipient_cd_original",
        "prime_award_transaction_recipient_county_fips_code",
        "prime_award_transaction_recipient_state_fips_code",
        "product_or_service_code",
        "product_or_service_code_description",
        "recipient_address_line_1",
        "recipient_address_line_2",
        "recipient_city_name",
        "recipient_country_code",
        "recipient_country_name",
        "recipient_county_name",
        "recipient_name",
        "recipient_name_raw",
        "recipient_parent_name",
        "recipient_parent_name_raw",
        "recipient_parent_uei",
        "recipient_state_code",
        "recipient_state_name",
        "recipient_uei",
        "recipient_zip_4_code",
        "school_district_local_government",
        "state_controlled_institution_of_higher_learning",
        "township_local_government",
        "transaction_description",
        "us_local_government",
        "us_state_government",
        "us_tribal_government",
        "usaspending_permalink",
    ]
    assert results == expected_results


def test_get_date_ranges():
    # test simple default
    result = seed_helpers.get_date_ranges(
        start_date="2009-01-01", end_date="2010-01-31"
    )
    expected_result = [
        ("2009-01-01", "2009-12-31"),
        ("2010-01-01", "2010-01-31"),
    ]
    assert result == expected_result

    # test default ending on leap day
    result = seed_helpers.get_date_ranges(
        start_date="2015-02-01", end_date="2016-02-29"
    )
    expected_result = [
        ("2015-02-01", "2016-01-31"),
        ("2016-02-01", "2016-02-29"),
    ]
    assert result == expected_result

    # test < 12 months spanning across years
    result = seed_helpers.get_date_ranges(
        start_date="2009-10-01", end_date="2010-01-31"
    )
    expected_result = [("2009-10-01", "2010-01-31")]
    assert result == expected_result

    # test leap year on non middle tuple
    result = seed_helpers.get_date_ranges(
        start_date="2010-03-01", end_date="2014-02-28"
    )
    expected_result = [
        ("2010-03-01", "2011-02-28"),
        ("2011-03-01", "2012-02-29"),
        ("2012-03-01", "2013-02-28"),
        ("2013-03-01", "2014-02-28"),
    ]
    assert result == expected_result

    # test default end_date = today
    result = seed_helpers.get_date_ranges(start_date="2024-01-01")
    assert result[-1][-1] == datetime.today().strftime("%Y-%m-%d")

    # test start_date before end_date
    with pytest.raises(ValueError) as e:
        seed_helpers.get_date_ranges(start_date="2024-01-02", end_date="2024-01-01")

    # test final period less than 1 year on leapday.
    result = seed_helpers.get_date_ranges(
        start_date="2019-01-01", end_date="2020-02-29"
    )
    expected_result = [("2019-01-01", "2019-12-31"), ("2020-01-01", "2020-02-29")]
    assert result == expected_result


def test_get_awards_payload():
    expected_results = [
        {
            "columns": list(
                set(seed_helpers.get_raw_columns(AssistanceTransactions))
                | set(seed_helpers.get_raw_columns(ProcurementTransactions))
            ),
            "file_format": "csv",
            "filters": {
                "agencies": [{"name": "All", "tier": "toptier", "type": "awarding"}],
                "date_range": {"start_date": "2022-10-01", "end_date": "2023-09-30"},
                "date_type": "action_date",
                "prime_award_types": seed_helpers.PRIME_AWARD_TYPES,
            },
        },
        {
            "columns": list(
                set(seed_helpers.get_raw_columns(AssistanceTransactions))
                | set(seed_helpers.get_raw_columns(ProcurementTransactions))
            ),
            "file_format": "csv",
            "filters": {
                "agencies": [{"name": "All", "tier": "toptier", "type": "awarding"}],
                "date_range": {"start_date": "2023-10-01", "end_date": "2023-10-31"},
                "date_type": "action_date",
                "prime_award_types": seed_helpers.PRIME_AWARD_TYPES,
            },
        },
    ]
    results = seed_helpers.get_awards_payloads(
        start_date="2022-10-01", end_date="2023-10-31"
    )
    assert results == expected_results


def test_generate_copy_from_sql():
    test_cols = {
        "asst_cols": ["asst_col1", "asst_col2"],
        "proc_cols": ["proc_col1", "proc_col2"],
    }
    result = seed_helpers.generate_copy_from_sql("Assistance_1.csv", test_cols)
    expected_result = "COPY assistance_transactions(asst_col1, asst_col2) FROM STDIN WITH (FORMAT CSV, HEADER)"
    assert result == expected_result
    result = seed_helpers.generate_copy_from_sql("Contract_1.csv", test_cols)
    expected_result = "COPY procurement_transactions(proc_col1, proc_col2) FROM STDIN WITH (FORMAT CSV, HEADER)"
    assert result == expected_result
    # test file name exception
    with pytest.raises(ValueError):
        seed_helpers.generate_copy_from_sql("invalid_fname")
    # test test_cols keys exception
    with pytest.raises(ValueError):
        seed_helpers.generate_copy_from_sql("Assistance", {"invalid_key": ["foo"]})
