from collections import OrderedDict
from factory import Factory
import datetime
from awardsreport.models import ProcurementTransactions, AssistanceTransactions
from faker import Faker

fake = Faker()


def generate_contract_award_unique_key():
    """Generate realistic contract award unique key values.

    See USAspending data dictionary PrimeAwardUniqueKey
    (https://www.usaspending.gov/data-dictionary)

    return str
    """
    piid = fake.pystr(5, 10)
    agency_id = fake.bothify("###")
    parent_piid = fake.random_element(
        elements=OrderedDict([(fake.pystr(5, 10), 0.5), ("NONE", 0.5)])
    )
    idv_agency_id = fake.bothify("###") if parent_piid != "NONE" else "NONE"
    return "_".join((piid, agency_id, parent_piid, idv_agency_id))


def generate_asisstance_award_unique_key():
    """Generate realistic assistance award unique key values.

    See USAspending data dictionary PrimeAwardUniqueKey
    (https://www.usaspending.gov/data-dictionary)

    return str
    """
    fain = fake.pystr(5, 10)
    uri = fake.random_element(
        elements=OrderedDict([(fake.pystr(5, 10), 0.5), ("NONE", 0.5)])
    )
    aw_ag_sub_code = fake.bothify("###")
    return "_".join((fain, uri, aw_ag_sub_code))


class BaseTransactionsFactory(Factory):
    class Meta:
        abstract = True

    action_date = fake.date_between(
        datetime.date(2022, 5, 1), datetime.date(2023, 5, 31)
    )
    awarding_agency_code = fake.bothify("####")
    awarding_agency_name = fake.pystr(5, 10)
    awarding_office_code = fake.bothify("######")
    awarding_office_name = fake.pystr(5, 10)
    awarding_sub_agency_code = fake.bothify("####")
    awarding_sub_agency_name = fake.pystr(5, 10)
    federal_action_obligation = fake.pyfloat(
        right_digits=2, min_value=-100, max_value=100
    )
    primary_place_of_performance_congressional_district = (
        f"{fake.state_abbr()} - {fake.bothify('##')}"
    )
    primary_place_of_performance_country_code = fake.bothify("#####")
    primary_place_of_performance_country_name = fake.country()
    primary_place_of_performance_county_name = fake.pystr(5, 10)
    primary_place_of_performance_state_name = fake.state()
    prime_award_transaction_place_of_performance_county_fips_code = fake.bothify(
        "#####"
    )
    prime_award_transaction_place_of_performance_state_fips_code = fake.bothify("##")


class AssistanceTransactionsFactory(BaseTransactionsFactory):
    class Meta:
        model = AssistanceTransactions

    assistance_award_unique_key = generate_asisstance_award_unique_key()
    assistance_type_code = fake.bothify("##")
    cfda_number = fake.bothify("##.###")
    cfda_title = fake.pystr(5, 10)
    original_loan_subsidy_cost = fake.pyfloat(
        right_digits=2, positive=True, max_value=100
    )


class ProcurementTransactionsFactory(BaseTransactionsFactory):
    class Meta:
        model = ProcurementTransactions

    contract_award_unique_key = generate_contract_award_unique_key()
