from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from typing import Literal, get_args, Tuple, Dict, List, Type, Optional
from awardsreport.models import (
    AssistanceTransactions,
    AssistanceTransactionsMixin,
    ProcurementTransactions,
    ProcurementTransactionsMixin,
    TransactionsMixin,
)
from awardsreport.schemas import seed_helpers_schemas


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
) -> list[str]:
    """Get non-derived, non-Id columns from specified table.

    args
        table: Type[AssistanceTransactions] | Type[ProcurementTransactions] the
        table from which to retrieve the raw columns.

    raises
        ValueError if table not in (AssistanceTransactions, ProcurementTransactions)

    returns list[str] sorted columns from table that come directly from the source data.
    """
    if table not in (AssistanceTransactions, ProcurementTransactions):
        raise ValueError(
            f"invalid table {table}, expected one of (AssistanceTransactions, ProcurementTransactions"
        )
    asst_proc_tx_cols = (
        AssistanceTransactionsMixin.__annotations__
        if table == AssistanceTransactions
        else ProcurementTransactionsMixin.__annotations__
    )
    tx_cols = TransactionsMixin.__annotations__
    return sorted([*asst_proc_tx_cols, *tx_cols])


def get_date_ranges(
    start_date: str, end_date: Optional[str] = None
) -> List[Tuple[str, str]]:
    """Get list of date ranges for start_date and end_date parameters for
    api/v2/bulk_downloads/awards.

    The first date of the first tuple is start_date. The last date of the last
    tuple is end_date. The last date of each tuple is less than 1 year after the
    first date. This is necessary since the api/v2/bulk_downloads/awards
    endpoint only accepts date ranges within a year. The first date in each
    tuple is one day after the last date of the preceding tuple. Dates are
    formatted as YYYY-MM-DD.

    args
        start_date: Earliest date in range format as YYYY-MM-DD.
        end_date: Last date in range format as YYYY-MM-DD.

    returns
        list of date ranges, each less than 1 year from start_date to end_date.
    """
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    if start > end:
        raise ValueError("start_date must less than or equal to end_date")

    current_start = start
    date_ranges: List[Tuple[str, str]] = []
    while current_start < end - relativedelta(years=1):
        date_ranges.append(
            (
                current_start.strftime("%Y-%m-%d"),
                (
                    current_start + relativedelta(years=1) - relativedelta(days=1)
                ).strftime("%Y-%m-%d"),
            )
        )
        current_start = current_start + relativedelta(years=1)

    date_ranges.append((current_start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))

    return date_ranges


def get_awards_payloads(
    start_date: str, end_date: Optional[str] = None
) -> list[seed_helpers_schemas.AwardsPayload]:
    """Generate payloads for USAs awards download from start_date to end_date.

    Download data from https://api.usaspending.gov/api/v2/bulk_download/awards/

    args
        start_date: Earliest date in range format as YYYY-MM-DD.
        end_date: Last date in range format as YYYY-MM-DD.

    returns list[seed_helpers_schemas.AwardsPayload]for api/v2/bulk_downloads/awards/
    """
    return [
        seed_helpers_schemas.AwardsPayload(
            columns=list(
                set(get_raw_columns(AssistanceTransactions))
                | set(get_raw_columns(ProcurementTransactions))
            ),
            filters=seed_helpers_schemas.AwardsPayloadFilters(
                prime_award_types=PRIME_AWARD_TYPES,
                date_type="action_date",
                date_range=seed_helpers_schemas.AwardsPayloadFilterDateRange(
                    start_date=start_date,
                    end_date=end_date,
                ),
                agencies=[seed_helpers_schemas.AwardsPayloadFilterAgencies()],
            ),
        )
        for start_date, end_date in get_date_ranges(start_date, end_date)
    ]


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
