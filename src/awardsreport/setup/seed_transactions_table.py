from sqlalchemy import select, column, union_all, literal_column
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
    mixin_cols = [col for col in mixin.__annotations__.keys()]
    return [literal_column("NULL").label(col) for col in mixin_cols]


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

    asst_tx_sel = select(
        *tx_mixin_cols,
        *tx_deriv_cols,
        *get_tx_cols_none(ProcurementTransactionsMixin),
        *tx_asst_mixin_cols,
    ).select_from(AssistanceTransactions)

    proc_tx_sel = select(
        *tx_mixin_cols,
        *tx_deriv_cols,
        *tx_proc_mixin_cols,
        *get_tx_cols_none(AssistanceTransactionsMixin),
    ).select_from(ProcurementTransactions)

    sel = asst_tx_sel.union_all(proc_tx_sel)
    session.execute(
        Base.metadata.tables["transactions"].insert()
        # the last column in transactions is id, it should not be inserted.
        .from_select(Base.metadata.tables["transactions"].c.keys()[:-1], sel)
    )
    session.commit()
