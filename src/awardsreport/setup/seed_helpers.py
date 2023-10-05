from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Literal, get_args, Tuple, Dict, List, Type, Annotated
from awardsreport.models import (
    AssistanceTransactions,
    ProcurementTransactions,
    TransactionDerivationsMixin,
)


file_types = Literal["assistance", "procurement"]
TODAY = date.today()
YEAR = TODAY.year
MONTH = TODAY.month - 1
VALID_FILE_TYPES: Tuple[file_types, ...] = get_args(file_types)
USER_AGENT = {"User-Agent": "Mozilla/5.0"}
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


def get_raw_columns(
    table: Type[AssistanceTransactions] | Type[ProcurementTransactions],
):
    table_cols = table.__table__.columns.keys()
    derived_cols = TransactionDerivationsMixin.__annotations__
    return sorted([key for key in table_cols if key not in derived_cols])


def get_date_ranges(
    year: int,
    month: int,
    no_months: int = 13,
    period_months: int = 12,
) -> list[tuple[str]]:
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
        no_months int the number of months prior of the first date, default 13
        period_months int maximum number of months between dates in tuple,
        default 12

    raises
        ValueError if no_months <= 0
        ValueError if period_months > 12
    """
    if no_months <= 0:
        raise ValueError("no_months must be greater than 0.")
    if period_months > 12:
        raise ValueError("period_months must be <= 12")
    date_ranges = []
    ymd = "%Y-%m-%d"
    end_date = date(year, month, 1) + relativedelta(months=1) - relativedelta(days=1)
    start_date = end_date + relativedelta(days=1) - relativedelta(months=no_months)
    current_end = (
        start_date + relativedelta(months=period_months) - relativedelta(days=1)
    )
    while current_end < end_date:
        date_ranges.append((start_date.strftime(ymd), current_end.strftime(ymd)))
        start_date = current_end + relativedelta(days=1)
        current_end = (
            start_date + relativedelta(months=period_months) - relativedelta(days=1)
        )
    date_ranges.append((start_date.strftime(ymd), end_date.strftime(ymd)))
    return date_ranges


def get_awards_payloads(year, month, no_months, period_months):
    """Generate payloads for USAs awards download for full months no_months
    before the last day of the specified month.

    Download data from https://api.usaspending.gov/api/v2/bulk_download/awards/

    args
        year int the last year of the last date range.
        month int the last month of the last date range.
        no_months int the number of months prior of the first date.

    returns list of dict suitable as payloads for api/v2/bulk_downloads/awards/
    """
    date_ranges = get_date_ranges(year, month, no_months, period_months)
    payloads = [
        {
            "columns": list(
                set(get_raw_columns(AssistanceTransactions))
                | set(get_raw_columns(ProcurementTransactions))
            ),
            "filters": {
                "prime_award_types": PRIME_AWARD_TYPES,
                "date_type": "action_date",
                "date_range": {f"start_date": start_date, "end_date": end_date},
                "agencies": [{"type": "awarding", "tier": "toptier", "name": "All"}],
            },
            "file_format": "csv",
        }
        for start_date, end_date in date_ranges  # type: ignore
    ]
    return payloads


def generate_copy_from_sql(
    fname: str, test_cols: Dict[str, List[str]] | None = None
) -> str:
    """Generate sql COPY FROM command to insert to psql.

    If fname contains 'Assistance' insert into assistance_transactions.
    If fname contains 'Contract' insert into procurement_transactions.

    args
        fname str file name to insert
        test_cols TestColsType COPY columns to simplify testing. Users should
        not need to interact with this parameter.

    return str valid postgresql COPY FROM statement to insert data from fname to appropriate table.

    raises
        ValueError if provided test_col keys are not exactly 'asst_cols' and 'proc_cols'.
        ValueError if fname does not inclue 'Assistance' or 'Contract'
    """
    if test_cols:
        valid_keys = {"asst_cols", "proc_cols"}
        test_col_keys = test_cols.keys()
        if set(test_col_keys) != (valid_keys):
            raise ValueError(
                f"invalid test_cols keys: {test_col_keys}. test_col keys must be 'asst_cols' and 'proc_cols'"
            )
        asst_cols = test_cols["asst_cols"]
        proc_cols = test_cols["proc_cols"]
    else:
        asst_cols = get_raw_columns(AssistanceTransactions)
        proc_cols = get_raw_columns(ProcurementTransactions)

    if "Assistance" in fname:
        cols = ", ".join(asst_cols)
        table_name = "assistance_transactions"
    elif "Contract" in fname:
        cols = ", ".join(proc_cols)
        table_name = "procurement_transactions"
    else:
        raise ValueError(
            f"invalid fname: {fname}. fname must include substring 'Assistance' or 'Contract'"
        )
    return f"COPY {table_name}({cols}) FROM STDIN WITH (FORMAT CSV, HEADER)"
