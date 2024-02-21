from enum import Enum

from util import JSONError, get_contract_signature, get_fair, status

from register.models import SignupContract
from fair.models import RegistrationState
from accounting.models import Order


class RegistrationType(Enum):
    BeforeInitialRegistration = 0
    InitialRegistration = 1
    InitialRegistrationSigned = 2
    AfterInitialRegistration = 3
    AfterInitialRegistrationSigned = 4
    BeforeCompleteRegistration = 5
    CompleteRegistration = 6
    CompleteRegistrationSigned = 7
    AfterCompleteRegistration = 8
    AfterCompleteRegistrationSigned = 9

    def __str__(self):
        if self == RegistrationType.BeforeInitialRegistration:
            return "before_initial_registration"
        elif self == RegistrationType.InitialRegistration:
            return "initial_registration"
        elif self == RegistrationType.InitialRegistrationSigned:
            return "initial_registration_signed"
        elif self == RegistrationType.AfterInitialRegistration:
            return "after_initial_registration"
        elif self == RegistrationType.AfterInitialRegistrationSigned:
            return "after_initial_registration_signed"
        if self == RegistrationType.BeforeCompleteRegistration:
            return "before_complete_registration"
        if self == RegistrationType.CompleteRegistration:
            return "complete_registration"
        elif self == RegistrationType.CompleteRegistrationSigned:
            return "complete_registration_signed"
        elif self == RegistrationType.AfterCompleteRegistration:
            return "after_complete_registration"
        elif self == RegistrationType.AfterCompleteRegistrationSigned:
            return "after_complete_registration_signed"
        else:
            return "unknown"


class Registration:
    def __init__(self, company, exhibitor, contact, fair, orders):
        self.company = company
        self.exhibitor = exhibitor
        self.contact = contact
        self.fair = fair
        self.orders = orders

        cr_contract, cr_signature = get_contract_signature(company, fair, "COMPLETE")
        self.cr_contract = cr_contract
        self.cr_signature = cr_signature

        ir_contract, ir_signature = get_contract_signature(company, fair, "INITIAL")
        self.ir_contract = ir_contract
        self.ir_signature = ir_signature

        period = fair.get_period()

        if period == RegistrationState.BEFORE_IR:
            pass
        elif period == RegistrationState.IR:
            self.ensure_ir_eligibility()

            self.deadline = fair.registration_end_date

            if ir_contract == None:
                self.type = RegistrationType.BeforeCompleteRegistration
            elif ir_signature != None:
                self.type = RegistrationType.InitialRegistrationSigned
            else:
                self.type = RegistrationType.InitialRegistration
        elif period == RegistrationState.AFTER_IR:
            self.ensure_ir_eligibility()

            if ir_signature != None:
                self.type = RegistrationType.AfterInitialRegistrationSigned
            else:
                self.type = RegistrationType.AfterInitialRegistration
        elif period == RegistrationState.CR:
            self.ensure_cr_eligibility()

            self.deadline = (
                exhibitor.deadline_complete_registration
                or fair.complete_registration_close_date
            )
            if cr_contract == None:
                self.type = RegistrationType.BeforeCompleteRegistration
            elif cr_signature != None:
                self.type = RegistrationType.CompleteRegistrationSigned
            else:
                self.type = RegistrationType.CompleteRegistration
        elif period == RegistrationState.AFTER_CR:
            self.ensure_cr_eligibility()

            if cr_contract == None:
                # This should not happen in a normal fair
                # This means FR is over, but there is no contract
                self.type = RegistrationType.BeforeCompleteRegistration
            elif cr_signature != None:
                self.type = RegistrationType.AfterCompleteRegistrationSigned
            else:
                self.type = RegistrationType.AfterCompleteRegistration
        else:
            pass

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
                raise JSONError(
                    status.USER_DID_NOT_SIGN_IR
                )  # Todo: allow company to bypass this
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
