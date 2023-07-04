from sqlalchemy import String, Float, Date
from sqlalchemy.orm import mapped_column

from awardsreport.database import Base


class AssistanceTransactions(Base):
    __tablename__ = "assistance_transactions"

    # These columns must be declared alphabetically and match
    # seed_helpers.ASSISTANCE_COLS in name and order.
    # This is because the download endpoint returns columns in alphabetical
    # order when columns are specified.
    # This also prevents us from using a abstract class for shared columns
    # betwenn AssistanceTransactions and ContractTransactions.
    action_date = mapped_column(Date)
    assistance_award_unique_key = mapped_column(String, nullable=False)
    assistance_transaction_unique_key = mapped_column(
        String, primary_key=True, autoincrement=False
    )
    assistance_type_code = mapped_column(String(2))
    awarding_agency_code = mapped_column(String(4))
    awarding_agency_name = mapped_column(String)
    awarding_office_code = mapped_column(String(6))
    awarding_office_name = mapped_column(String)
    awarding_sub_agency_code = mapped_column(String(4))
    awarding_sub_agency_name = mapped_column(String)
    cfda_number = mapped_column(String(6))
    cfda_title = mapped_column(String)
    federal_action_obligation = mapped_column(Float)
    original_loan_subsidy_cost = mapped_column(Float)
    primary_place_of_performance_congressional_district = mapped_column(String)
    primary_place_of_performance_country_code = mapped_column(String)
    primary_place_of_performance_country_name = mapped_column(String)
    primary_place_of_performance_county_name = mapped_column(String)
    primary_place_of_performance_state_name = mapped_column(String)
    prime_award_transaction_place_of_performance_county_fips_code = mapped_column(
        String(5)
    )
    prime_award_transaction_place_of_performance_state_fips_code = mapped_column(
        String(2)
    )


class ProcurementTransactions(Base):
    __tablename__ = "procurement_transactions"

    action_date = mapped_column(Date)
    awarding_agency_code = mapped_column(String(4))
    awarding_agency_name = mapped_column(String)
    awarding_office_code = mapped_column(String(6))
    awarding_office_name = mapped_column(String)
    awarding_sub_agency_code = mapped_column(String(4))
    awarding_sub_agency_name = mapped_column(String)
    contract_award_unique_key = mapped_column(String, nullable=False)
    contract_transaction_unique_key = mapped_column(String, primary_key=True)
    federal_action_obligation = mapped_column(Float)
    primary_place_of_performance_congressional_district = mapped_column(String)
    primary_place_of_performance_country_code = mapped_column(String)
    primary_place_of_performance_country_name = mapped_column(String)
    primary_place_of_performance_county_name = mapped_column(String)
    primary_place_of_performance_state_name = mapped_column(String)
    prime_award_transaction_place_of_performance_county_fips_code = mapped_column(
        String(5)
    )
    prime_award_transaction_place_of_performance_state_fips_code = mapped_column(
        String(2)
    )
