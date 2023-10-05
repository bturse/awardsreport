from sqlalchemy import select, column, text
from awardsreport.database import sess, Base

from awardsreport.models import (
    TransactionsMixin,
    AssistanceTransactions,
    TransactionDerivationsMixin,
    ProcurementTransactions,
    ProcurementTransactionsMixin,
    AssistanceTransactionsMixin,
)


def get_tx_cols_none(mixin=None):
    mixin_cols = [column(col) for col in mixin.__annotations__.keys()]
    return ", ".join(f"NULL as {col}" for col in mixin_cols)


tx_mixin_cols = [column(col) for col in TransactionsMixin.__annotations__.keys()]
tx_deriv_cols = [
    column(col) for col in TransactionDerivationsMixin.__annotations__.keys()
]
tx_proc_mixin_cols = [
    column(col) for col in ProcurementTransactionsMixin.__annotations__.keys()
]
tx_asst_mixin_cols = [
    column(col) for col in AssistanceTransactionsMixin.__annotations__.keys()
]

if __name__ == "__main__":
    session = sess()

    sel = (
        select(
            *tx_mixin_cols,
            *tx_deriv_cols,
            *tx_proc_mixin_cols,
            text(get_tx_cols_none(AssistanceTransactionsMixin)),
        )
        .select_from(ProcurementTransactions)
        .union_all(
            select(
                *tx_mixin_cols,
                *tx_deriv_cols,
                text(get_tx_cols_none(ProcurementTransactionsMixin)),
                *tx_asst_mixin_cols,
            ).select_from(AssistanceTransactions)
        )
    )

    session.execute(
        Base.metadata.tables["transactions"].insert()
        # the last column in transactions is id, it should not be inserted.
        .from_select(Base.metadata.tables["transactions"].c.keys()[:-1], sel)
    )
    session.commit()
