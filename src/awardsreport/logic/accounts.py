from sqlalchemy import select, func, desc, create_engine
from awardsreport.models import FederalAccountBalance
from awardsreport.database import Session


def fab_dif(fy, period):
    last_fy = str(int(fy) - 1)
    fy_cte = (
        select(FederalAccountBalance)
        .where(FederalAccountBalance.fiscal_year == fy)
        .cte()
    )
    lfy_cte = (
        select(FederalAccountBalance)
        .where(FederalAccountBalance.fiscal_year == last_fy)
        .cte()
    )

    stmt = (
        select(
            fy_cte.c.federal_account_symbol,
            (
                fy_cte.c.total_budgetary_resources - lfy_cte.c.total_budgetary_resources
            ).label("ob_dif"),
            (
                func.abs(
                    fy_cte.c.total_budgetary_resources
                    - lfy_cte.c.total_budgetary_resources
                )
            ).label("abs_ob_dif"),
        )
        .select_from(fy_cte)
        .join(
            lfy_cte, fy_cte.c.federal_account_symbol == lfy_cte.c.federal_account_symbol
        )
        .order_by(desc("abs_ob_dif"))
    )

    with Session.begin() as sess:
        return sess.execute(stmt)
