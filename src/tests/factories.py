from collections import OrderedDict
from factory import Factory, Sequence
import datetime
from awardsreport.models import (
    ProcurementTransactions,
    AssistanceTransactions,
    Transactions,
)
from faker import Faker

fake = Faker()


def generate_contract_award_unique_key() -> str:
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


def generate_asisstance_award_unique_key() -> str:
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


class HasIdFactory:
    class Meta:
        abstract = True

    id = Sequence(lambda n: n)


class TransactionsMixinFactory(Factory):
    class Meta:
        abstract = True

    action_date = fake.date_between(
        datetime.date(2022, 5, 1), datetime.date(2023, 5, 31)
    )
    awarding_agency_code = fake.bothify("####")
    awarding_agency_name = fake.pystr(5, 10)
    federal_action_obligation = fake.pyfloat(
        right_digits=2, min_value=-100, max_value=100
    )
    primary_place_of_performance_state_name = fake.state()
    recipient_name = fake.pystr(5, 10)
    recipient_uei = fake.pystr(5, 10)
    usaspending_permalink = fake.pystr(5, 10)


class ProcurementTransactionsMixinFactory(Factory):
    class Meta:
        abstract = True

    contract_award_unique_key = generate_contract_award_unique_key()
    contract_transaction_unique_key = Sequence(lambda n: n)
    naics_code = fake.bothify("##.###")
    naics_description = fake.pystr(5, 10)
    product_or_service_code = fake.bothify("######")
    product_or_service_code_description = fake.pystr(5, 10)


class AssistanceTransactionsMixinFactory(Factory):
    class Meta:
        abstract = True

    assistance_award_unique_key = generate_asisstance_award_unique_key()
    assistance_transaction_unique_key = Sequence(lambda n: n)
    assistance_type_code = fake.bothify("##")
    cfda_number = fake.bothify("##.###")
    cfda_title = fake.pystr(5, 10)
    original_loan_subsidy_cost = fake.pyfloat(
        right_digits=2, positive=True, max_value=100
    )


class TransactionDerivationsMixinFactory(Factory):
    class Meta:
        abstract = True

    generated_pragmatic_obligations = fake.pyfloat(right_digits=2, max_value=100)
    action_date_month = fake.pyint(1, 12)
    action_date_year = fake.pyint(2008, 2023)
    award_summary_unique_key = Sequence(lambda n: n)


class AssistanceTransactionsFactory(
    TransactionsMixinFactory,
    AssistanceTransactionsMixinFactory,
    HasIdFactory,
    TransactionDerivationsMixinFactory,
):
    class Meta:
        model = AssistanceTransactions


class ProcurementTransactionsFactory(
    TransactionsMixinFactory,
    ProcurementTransactionsMixinFactory,
    HasIdFactory,
    TransactionDerivationsMixinFactory,
):
    class Meta:
        model = ProcurementTransactions


class TransactionsFactory(
    TransactionsMixinFactory,
    TransactionDerivationsMixinFactory,
    ProcurementTransactionsMixinFactory,
    AssistanceTransactionsMixinFactory,
    HasIdFactory,
):
    class Meta:
        model = Transactions
