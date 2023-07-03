from awardsreport.database import Session
from awardsreport.models import ProcurementTransactions, AssistanceTransactions
from awardsreport.helpers.seed_helpers import YEAR, MONTH
from sqlalchemy import select, func, desc, extract


def get_award_type_month_total(award_type: str, year: int = YEAR, month: int = MONTH):
    """Get the sum of the specified award type spending in the specified year and month.

    Loan spending is measures with original loan subsidy cost. Non-loan
    financial assistance and procurement spending is measured with federal
    action obligation.

    args:
        award_type str type of award spending to sum. One of 'assistance,'
        'loan,' or 'procurement.' If assistance, sum non-loan assistance
        obligations. If loan, sum loan subsidy cost. If procurement sum
        procurement obligations.
        year int year of spending to sum, defaults to year of last month.
        month int month on spending to sum, defaults to last month.

    return float

    raises
        ValueError if sum_col not in: 'assistance,' 'loan,' 'procurement'
    """
    if award_type not in ("assistance," "loan," "procurement"):
        raise ValueError("award_type must be one of: assistance, loan, or procurement")

    session = Session()
    type_cols = {
        "assistance": AssistanceTransactions.federal_action_obligation,
        "loan": AssistanceTransactions.original_loan_subsidy_cost,
        "procurement": ProcurementTransactions.federal_action_obligation,
    }
    sum_col = type_cols[award_type]
    sum_tbl = sum_col.parent.class_

    stmt = select(func.sum(sum_col)).filter(
        extract("year", sum_tbl.action_date) == year,
        extract("month", sum_tbl.action_date) == month,
    )
    if award_type == "loan":
        stmt = stmt.where(sum_tbl.assistance_type_code.in_(("07", "08")))
    results = session.scalar(stmt)
    return results


# todo: create a schema for returned object
def get_month_totals(year: int = YEAR, month: int = MONTH):
    """Get total spending in specified year and month.

    args:
        year int year of spending to sum
        month int month on spending to sum

    returns dict


    """
    month_totals = {
        "assistance": get_award_type_month_total("assistance", year, month),
        "loan": get_award_type_month_total("loan", year, month),
        "procurement": get_award_type_month_total("procurement", year, month),
    }
    return {
        "year": year,
        "month": month,
        "total": month_totals["assistance"]
        + month_totals["loan"]
        + month_totals["procurement"],
        "award_type_totals": month_totals,
    }


def get_agency_obligations(record_limit: int = 3):
    session = Session()
    stmt = (
        select(
            ProcurementTransactions.awarding_agency_name,
            func.sum(ProcurementTransactions.federal_action_obligation).label(
                "sum_obl"
            ),
        )
        .group_by(ProcurementTransactions.awarding_agency_name)
        .order_by(desc("sum_obl"))
        .limit(record_limit)
    )
    results = session.execute(stmt).all()
    ag_ob = [
        {
            "awarding_agency_name": result.awarding_agency_name,
            "sum_obl": result.sum_obl,
        }
        for result in results
    ]
    return ag_ob