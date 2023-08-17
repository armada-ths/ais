from register.models import SignupContract
from util import JSONError, get_contract_signature, get_fair, status

from enum import Enum

from fair.models import RegistrationState


class RegistrationType(Enum):
    BeforeCompleteRegistration = 0
    CompleteRegistration = 1
    CompleteRegistrationSigned = 2

    def __str__(self):
        if self == RegistrationType.BeforeCompleteRegistration:
            return "before_complete_registration"
        if self == RegistrationType.CompleteRegistration:
            return "complete_registration"
        elif self == RegistrationType.CompleteRegistrationSigned:
            return "complete_registration_signed"


class Registration:
    def __init__(self, company, exhibitor, contact, fair, orders):
        self.company = company
        self.exhibitor = exhibitor
        self.contact = contact
        self.fair = fair
        self.orders = orders

        contract, signature = get_contract_signature(company, fair, "COMPLETE")
        self.contract = contract
        self.signature = signature

        ir_contract, ir_signature = get_contract_signature(company, fair, "INITIAL")
        self.ir_contract = ir_contract
        self.ir_signature = ir_signature

        period = fair.get_period()

        if period == RegistrationState.BEFORE_IR:
            pass
        elif period == RegistrationState.IR:
            pass
        elif period == RegistrationState.AFTER_IR:
            pass
        elif period == RegistrationState.CR:
            self.ensure_cr_eligibility()

            self.deadline = (
                exhibitor.deadline_complete_registration
                or fair.complete_registration_close_date
            )
            if contract == None:
                self.type = RegistrationType.BeforeCompleteRegistration
            elif signature != None:
                self.type = RegistrationType.CompleteRegistrationSigned
            else:
                self.type = RegistrationType.CompleteRegistration
        elif period == RegistrationState.AFTER_CR:
            pass
        else:
            pass

    def ensure_cr_eligibility(self):
        complete_contract = SignupContract.objects.filter(
            fair=get_fair(), type="COMPLETE", current=True
        ).first()
        if complete_contract == None:
            raise JSONError(status.CR_NOT_OPEN)

        signature = self.ir_signature

        if self.exhibitor == None:
            if signature == None:
                raise JSONError(status.USER_DID_NOT_SIGN_IR)
            else:
                raise JSONError(status.USER_IS_NOT_EXHIBITOR)
