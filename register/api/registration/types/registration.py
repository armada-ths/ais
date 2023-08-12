from enum import Enum

from fair.models import RegistrationState
from register.api import status

from register.api.registration.util import JSONError


class RegistrationType(Enum):
    CompleteRegistration = 1
    CompleteRegistrationSigned = 2

    def __str__(self):
        if self == RegistrationType.CompleteRegistration:
            return "complete_registration"
        elif self == RegistrationType.CompleteRegistrationSigned:
            return "complete_registration_signed"


class Registration:
    def __init__(self, company, exhibitor, contact, fair, contract, orders, signature):
        self.company = company
        self.exhibitor = exhibitor
        self.contact = contact
        self.fair = fair
        self.contract = contract
        self.orders = orders
        self.signature = signature

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

            if signature != None:
                self.type = RegistrationType.CompleteRegistrationSigned
            else:
                self.type = RegistrationType.CompleteRegistration
        elif period == RegistrationState.AFTER_CR:
            pass
        else:
            pass

    def ensure_cr_eligibility(self):
        if self.exhibitor == None:
            if self.signature == None:
                raise JSONError(status.USER_DID_NOT_SIGN_IR)
            else:
                raise JSONError(status.USER_IS_NOT_EXHIBITOR)
