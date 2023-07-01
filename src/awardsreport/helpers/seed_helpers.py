from typing import Literal, get_args, Tuple
from collections import namedtuple
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging

logging.basicConfig(filename=f"{__name__}.log", level=logging.INFO)
# https://stackoverflow.com/a/64522240/15363595
TODAY = date.today()
YEAR = TODAY.year
MONTH = TODAY.month

file_types = Literal["assistance", "procurement"]
VALID_FILE_TYPES: Tuple[file_types, ...] = get_args(file_types)

USER_AGENT = {"User-Agent": "Mozilla/5.0"}

ASSISTANCE_COLS = [
    "action_date",
    "assistance_award_unique_key",
    "assistance_transaction_unique_key",
    "assistance_type_description",
    "awarding_agency_code",
    "awarding_agency_name",
    "awarding_office_code",
    "awarding_office_name",
    "awarding_sub_agency_code",
    "awarding_sub_agency_name",
    "cfda_number",
    "cfda_title",
    "federal_action_obligation",
    "original_loan_subsidy_cost",
    "primary_place_of_performance_congressional_district",
    "primary_place_of_performance_country_code",
    "primary_place_of_performance_country_name",
    "primary_place_of_performance_county_name",
    "primary_place_of_performance_state_name",
    "prime_award_transaction_place_of_performance_county_fips_code",
    "prime_award_transaction_place_of_performance_state_fips_code",
]

PROCUREMENT_COLS = [
    "action_date",
    "awarding_agency_code",
    "awarding_agency_name",
    "awarding_office_code",
    "awarding_office_name",
    "awarding_sub_agency_code",
    "awarding_sub_agency_name",
    "contract_award_unique_key",
    "contract_transaction_unique_key",
    "federal_action_obligation",
    "primary_place_of_performance_congressional_district",
    "primary_place_of_performance_country_code",
    "primary_place_of_performance_country_name",
    "primary_place_of_performance_county_name",
    "primary_place_of_performance_state_name",
    "prime_award_transaction_place_of_performance_county_fips_code",
    "prime_award_transaction_place_of_performance_state_fips_code",
]

PRIME_AWARD_TYPES = [
    "A",
    "B",
    "C",
    "D",
    "IDV_A",
    "IDV_B",
    "IDV_B_A",
    "IDV_B_B",
    "IDV_B_C",
    "IDV_C",
    "IDV_D",
    "IDV_E",
    "02",
    "03",
    "04",
    "05",
    "10",
    "06",
    "07",
    "08",
    "09",
    "11",
]

AWARDS_DL_EP = "https://api.usaspending.gov/api/v2/bulk_download/awards/"


# def get_date_ranges(year: int, month: int):
#    """Get YYYY-mm-dd string for start, mid date, mid morrow date, and end dates for preceding 24 month range, given month and year.
#
#    Mid dates are necessary since the endpoint that will use these date ranges only supports 1 year of data per request.
#
#    args
#        year int end of range year.
#        month int end of range month
#
#    return collections.namedtuple DateRange(start_date, mid_date, mid_morrow_date, end_date)
#    """
#    DateRange = namedtuple("DateRange", "start_date mid_date mid_morrow_date end_date")
#    start_date = date(year=year - 2, month=month + 1, day=1)
#    end_date = date(year, month, 1) + relativedelta(months=1) - relativedelta(days=1)
#    mid_date = start_date + relativedelta(years=1) - relativedelta(days=1)
#    #    mid_date = start_date + (end_date - start_date) / 2
#    mid_morrow_date = mid_date + relativedelta(days=1)
#    return DateRange(
#        *map(
#            lambda d: d.strftime("%Y-%m-%d"),
#            [start_date, mid_date, mid_morrow_date, end_date],
#        )
#    )


def get_date_ranges(year: int, month: int, no_months: int):
    """Get list of date ranges for start_date and end_date parameters for
    api/v2/bulk_downloads/awards.

    The last date in the last tuple is the last day of the specified month in
    the specified year. The first date in the first tuple is the first day of
    the month no_months before the last date. The last date of each tuple is
    less than 1 year after the first date. This is necessary since the
    api/v2/bulk_downloads/awards endpoint only accepts date ranges within a
    year. The first date in each tuple is one day after the last date of the
    preceding tuple. Dates are formatted as "%Y-%m-%d".

    args
        year int the last year of the last date range.
        month int the last month of the last date range.
        no_months int the number of months prior of the first date.

    raises
        ValueError if no_months <= 0
    """
    if no_months <= 0:
        raise ValueError("no_months must be greater than 0.")
    date_ranges = []
    ymd = "%Y-%m-%d"
    end_date = date(year, month, 1) + relativedelta(months=1) - relativedelta(days=1)
    start_date = end_date + relativedelta(days=1) - relativedelta(months=no_months)
    current_end = start_date + relativedelta(years=1) - relativedelta(days=1)
    while current_end < end_date:
        date_ranges.append((start_date.strftime(ymd), current_end.strftime(ymd)))
        start_date = current_end + relativedelta(days=1)
        current_end = current_end + relativedelta(years=1) - relativedelta(days=1)
    date_ranges.append((start_date.strftime(ymd), end_date.strftime(ymd)))
    return date_ranges


def get_awards_payloads(year, month, no_months):
    """Generate payloads for USAs awards download for full months no_months
    before the last day of the specified month.

    Download data from https://api.usaspending.gov/api/v2/bulk_download/awards/

    args
        year int the last year of the last date range.
        month int the last month of the last date range.
        no_months int the number of months prior of the first date.

    returns list of dict suitable as payloads for api/v2/bulk_downloads/awards/
    """
    date_ranges = get_date_ranges(year, month, no_months)
    payloads = [
        {
            "columns": list(set(ASSISTANCE_COLS) | set(PROCUREMENT_COLS)),
            "filters": {
                "prime_award_types": PRIME_AWARD_TYPES,
                "date_type": "action_date",
                "date_range": {f"start_date": start_date, "end_date": end_date},
                "agencies": [{"type": "awarding", "tier": "toptier", "name": "All"}],
            },
            "file_format": "csv",
        }
        for start_date, end_date in date_ranges
    ]
    return payloads


def get_ep_split_award_payloads(year, month):
    pass
    """Get payloads with contiguous start and end dates for 24 month period.

    This is necessary since the api/v2/bulk_downloads/awards/ endpoint only
    accepts date ranges within a single year.

    args:
        year int
        month int

    returns dict with keys "endpoint" and "payloads."
    """
    start_date, mid_date, mid_morrow_date, end_date = get_date_ranges(year, month)
    return {
        "endpoint": AWARDS_DL_EP,
        "payloads": (
            # get_awards_payload(start_date, mid_date),
            # get_awards_payload(mid_morrow_date, end_date),
        ),
    }


def generate_copy_from_sql(file_type: file_types):
    """generate sql command to insert payload columns to table_name"""
    valid_file_types = ["assistance", "procurement"]
    if file_type not in VALID_FILE_TYPES:
        raise ValueError(f"file_type must be in {VALID_FILE_TYPES}")
    if file_type == "assistance":
        cols = ", ".join(ASSISTANCE_COLS)
        table_name = "assistance_transactions"
    elif file_type == "procurement":
        cols = ", ".join(PROCUREMENT_COLS)
        table_name = "procurement_transactions"
    return f"COPY {table_name}({cols}) FROM STDIN WITH (FORMAT CSV, HEADER)"
