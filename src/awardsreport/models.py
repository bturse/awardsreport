from sqlalchemy import String, Float, Date
from sqlalchemy.orm import mapped_column, Mapped

from awardsreport.database import Base


class TransactionsMixin:
    action_date: Mapped[Date] = mapped_column(Date)
    awarding_agency_code: Mapped[str] = mapped_column(String)
    awarding_agency_name: Mapped[str] = mapped_column(String)
    federal_action_obligation = mapped_column(Float)
    primary_place_of_performance_state_name = mapped_column(String)
    recipient_name = mapped_column(String)
    recipient_uei = mapped_column(String)
    usaspending_permalink = mapped_column(String)


class ProcurementTransactionsMixin:
    contract_award_unique_key = mapped_column(String, nullable=False)
    contract_transaction_unique_key = mapped_column(String, primary_key=True)
    naics_code = mapped_column(String)
    naics_description = mapped_column(String)
    product_or_service_code = mapped_column(String)
    product_or_service_code_description = mapped_column(String)


class AssistanceTransactionsMixin:
    assistance_award_unique_key = mapped_column(String, nullable=False)
    assistance_transaction_unique_key = mapped_column(String, primary_key=True)
    assistance_type_code = mapped_column(String(2))
    cfda_number = mapped_column(String(6))
    cfda_title = mapped_column(String)
    original_loan_subsidy_cost = mapped_column(Float)


class TransactionDerivationsMixin:
    generated_pragmatic_obligations = mapped_column(String)


class AssistanceTransactions(
    Base,
    TransactionsMixin,
    AssistanceTransactionsMixin,
    TransactionDerivationsMixin,  # must be inhereted last
):
    __tablename__ = "assistance_transactions"


class ProcurementTransactions(
    Base,
    TransactionsMixin,
    ProcurementTransactionsMixin,
    TransactionDerivationsMixin,  # must be inhereted last
):
    __tablename__ = "procurement_transactions"
