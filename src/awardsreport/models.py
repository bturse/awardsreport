from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from typing import Optional
from datetime import date

from awardsreport.database import Base


class HasId:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TransactionsMixin:
    action_date: Mapped[Optional[date]] = mapped_column(
        doc="""The date the action being reported was issued / signed by the
        Government or a binding agreement was reached."""
    )
    awarding_agency_code: Mapped[Optional[str]] = mapped_column(
        doc="""Code for agency which made the award. See <https://files.usaspending.gov/reference_data/agency_codes.csv>
        CGAC AGENCY CODE column"""
    )
    awarding_agency_name: Mapped[Optional[str]]
    federal_action_obligation: Mapped[Optional[float]]
    primary_place_of_performance_state_name: Mapped[Optional[str]] = mapped_column(
        doc="""Primary Place of Performance State. Two-letter abbreviation for the state or territory indicating
        where the predominant performance of the award will be accomplished."""
    )
    recipient_name: Mapped[Optional[str]]
    recipient_uei: Mapped[Optional[str]] = mapped_column(
        doc="""The Unique Entity Identifier (UEI) for an awardee or recipient. A
        UEI is a unique alphanumeric code used to identify a specific
        commercial, nonprofit, or business entity. See
        <https://www.fsd.gov/gsafsd_sp?id=kb_article_view&sysparm_article=KB0041255>"""
    )
    usaspending_permalink: Mapped[Optional[str]]


class ProcurementTransactionsMixin:
    contract_award_unique_key: Mapped[Optional[str]]
    contract_transaction_unique_key: Mapped[Optional[str]]
    naics_code: Mapped[Optional[str]] = mapped_column(
        String(6),
        doc="""The North American Industrial Classification System (NAICS) Code
        assigned to the solicitation and resulting award identifying the
        industry in which the contract requirements are normally performed. See
        <https://www.census.gov/naics/>""",
    )
    naics_description: Mapped[Optional[str]]
    product_or_service_code: Mapped[Optional[str]] = mapped_column(
        String(6),
        doc="""The 4-character code that best identifies the product or service procured.
        See <https://www.acquisition.gov/psc-manual>""",
    )
    product_or_service_code_description: Mapped[Optional[str]]


class AssistanceTransactionsMixin:
    assistance_award_unique_key: Mapped[Optional[str]]
    assistance_transaction_unique_key: Mapped[Optional[str]]
    assistance_type_code: Mapped[Optional[str]] = mapped_column(
        String(2), doc="""The type of assistance provided by the award."""
    )
    cfda_number: Mapped[Optional[str]] = mapped_column(
        String(6),
        doc="""The number assigned to an Assistance Listing in SAM.gov. See
        <https://sam.gov/content/assistance-listings>""",
    )
    cfda_title: Mapped[Optional[str]]
    original_loan_subsidy_cost: Mapped[Optional[float]]


class TransactionDerivationsMixin:
    generated_pragmatic_obligations: Mapped[Optional[float]]
    action_date_year_month: Mapped[Optional[str]] = mapped_column(
        doc="""'YYYY-MM' from `action_date`"""
    )
    action_date_year: Mapped[Optional[int]] = mapped_column(
        doc="""Year of `transaction.action_date`"""
    )
    award_summary_unique_key: Mapped[Optional[str]] = mapped_column(
        doc="""Uniquely identifies a procurement or assistance prime award
        summary."""
    )


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
