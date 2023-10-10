from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from typing import Optional
from datetime import date

from awardsreport.database import Base


class HasId:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TransactionsMixin:
    action_date: Mapped[Optional[date]]
    awarding_agency_code: Mapped[Optional[str]]
    awarding_agency_name: Mapped[Optional[str]]
    federal_action_obligation: Mapped[Optional[float]]
    primary_place_of_performance_state_name: Mapped[Optional[str]]
    recipient_name: Mapped[Optional[str]]
    recipient_uei: Mapped[Optional[str]]
    usaspending_permalink: Mapped[Optional[str]]


class ProcurementTransactionsMixin:
    contract_award_unique_key: Mapped[Optional[str]]
    contract_transaction_unique_key: Mapped[Optional[str]]
    naics_code: Mapped[Optional[str]] = mapped_column(String(6))
    naics_description: Mapped[Optional[str]]
    product_or_service_code: Mapped[Optional[str]] = mapped_column(String(6))
    product_or_service_code_description: Mapped[Optional[str]]


class AssistanceTransactionsMixin:
    assistance_award_unique_key: Mapped[Optional[str]]
    assistance_transaction_unique_key: Mapped[Optional[str]]
    assistance_type_code: Mapped[Optional[str]] = mapped_column(String(2))
    cfda_number: Mapped[Optional[str]] = mapped_column(String(6))
    cfda_title: Mapped[Optional[str]]
    original_loan_subsidy_cost: Mapped[Optional[float]]


class TransactionDerivationsMixin:
    generated_pragmatic_obligations: Mapped[Optional[float]]
    action_date_month: Mapped[Optional[int]]
    action_date_year: Mapped[Optional[int]]
    award_summary_unique_key: Mapped[Optional[str]]


class AssistanceTransactions(
    Base,
    TransactionsMixin,
    AssistanceTransactionsMixin,
    HasId,
    TransactionDerivationsMixin,  # must be inhereted last
):
    __tablename__ = "assistance_transactions"


class ProcurementTransactions(
    Base,
    TransactionsMixin,
    ProcurementTransactionsMixin,
    HasId,
    TransactionDerivationsMixin,  # must be inhereted last
):
    __tablename__ = "procurement_transactions"


class Transactions(
    Base,
    TransactionsMixin,
    TransactionDerivationsMixin,
    ProcurementTransactionsMixin,
    AssistanceTransactionsMixin,
    HasId,
):
    __tablename__ = "transactions"
