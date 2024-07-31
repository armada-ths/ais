from enum import Enum
from companies.models import Group

from util import JSONError, get_contract_signature, get_fair, get_sales_contacts, status

from register.models import SignupContract
from fair.models import RegistrationPeriod
from accounting.models import Order
from util.product import get_products


class Registration:
    def __init__(self, company, exhibitor, contact, fair, orders):
        self.company = company
        self.exhibitor = exhibitor
        self.contact = contact
        self.fair = fair
        self.orders = orders
        self.products = get_products(fair, company)

        cr_contract, cr_signature = get_contract_signature(company, fair, "COMPLETE")
        self.cr_contract = cr_contract
        self.cr_signature = cr_signature

        ir_contract, ir_signature = get_contract_signature(company, fair, "INITIAL")
        self.ir_contract = ir_contract
        self.ir_signature = ir_signature

        self.sales_contacts = get_sales_contacts(fair, company, exhibitor)
        self.interested_in = company.groups.filter(fair=fair, allow_registration=True)

        self.period = fair.get_period()

        if self.period == RegistrationPeriod.IR:
            self.ensure_ir_eligibility()
            self.deadline = fair.registration_end_date

        elif self.period == RegistrationPeriod.BETWEEN_IR_AND_CR:
            self.ensure_ir_eligibility()

        elif self.period == RegistrationPeriod.CR:
            self.ensure_cr_eligibility()

            self.deadline = (
                exhibitor.deadline_complete_registration
                or fair.complete_registration_close_date
            )

        elif self.period == RegistrationPeriod.AFTER_CR:
            self.ensure_cr_eligibility()

    def ensure_ir_eligibility(self):
        if self.ir_contract == None:
            raise JSONError(status.IR_NOT_OPEN)

    def ensure_cr_eligibility(self):
        complete_contract = SignupContract.objects.filter(
            fair=get_fair(), type="COMPLETE", current=True
        ).first()
        if complete_contract == None:
            raise JSONError(status.CR_NOT_OPEN)

        signature = self.ir_signature

        if self.exhibitor == None:
            if signature == None:
                # Todo: allow company to bypass this
                raise JSONError(status.USER_DID_NOT_SIGN_IR)
            else:
                raise JSONError(status.USER_IS_NOT_EXHIBITOR)


def get_registration(company, fair, contact, exhibitor):
    orders = Order.objects.filter(
        purchasing_company=company, product__revenue__fair=fair
    )

    return Registration(
        company=company,
        contact=contact,
        fair=fair,
        exhibitor=exhibitor,
        orders=orders,
    )
