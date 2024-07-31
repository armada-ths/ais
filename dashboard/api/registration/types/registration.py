from util import JSONError, get_contract_signature, get_fair, get_sales_contacts, status

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

        ir_contract, ir_signature = get_contract_signature(company, fair, "INITIAL")
        self.ir_contract = ir_contract
        self.ir_signature = ir_signature

        cr_contract, cr_signature = get_contract_signature(company, fair, "COMPLETE")
        self.cr_contract = cr_contract
        self.cr_signature = cr_signature

        self.sales_contacts = get_sales_contacts(fair, company, exhibitor)
        self.interested_in = company.groups.filter(fair=fair, allow_registration=True)

        self.period = fair.get_period()

        if self.period in [
            RegistrationPeriod.IR,
            RegistrationPeriod.BETWEEN_IR_AND_CR,
            RegistrationPeriod.CR,
            RegistrationPeriod.AFTER_CR,
        ]:
            self.ensure_ir_contract_exists()
        elif self.period in [RegistrationPeriod.CR, RegistrationPeriod.AFTER_CR]:
            self.ensure_cr_contract_exists()

    def ensure_ir_contract_exists(self):
        if self.ir_contract == None:
            raise JSONError(status.IR_NOT_OPEN)

    def ensure_cr_contract_exists(self):
        if self.cr_contract == None:
            raise JSONError(status.CR_NOT_OPEN)


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
