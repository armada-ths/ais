from enum import Enum
from rest_framework.fields import empty

from fair.models import RegistrationState

from register.api.registration.types.cr import (
    CRRegistrationSerializer,
    CRSignedRegistrationSerializer,
)
from register.api.registration.util import UserPermission, get_contract_signature


class RegistrationType(Enum):
    CompleteRegistration = 1
    CompleteRegistrationSigned = 2

    def __str__(self):
        if self == RegistrationType.CompleteRegistration:
            return "complete_registration"
        elif self == RegistrationType.CompleteRegistrationSigned:
            return "complete_registration_signed"


class Registration:
    def __init__(self, company, exhibitor, contact, fair, contract, orders):
        self.company = company
        self.exhibitor = exhibitor
        self.contact = contact
        self.fair = fair
        self.contract = contract
        self.orders = orders

        period = fair.get_period()

        if period == RegistrationState.BEFORE_IR:
            pass
        elif period == RegistrationState.IR:
            pass
        elif period == RegistrationState.AFTER_IR:
            pass
        elif period == RegistrationState.CR:
            _, signature = get_contract_signature(company, fair)

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

    def get_serializer(self, data=empty, context={}):
        user = context["user"]
        if user != None:
            permission = UserPermission(user)

        if self.type == RegistrationType.CompleteRegistration:
            Serializer = CRRegistrationSerializer
        elif self.type == RegistrationType.CompleteRegistrationSigned:
            # If user is sales, they may change anything he likes
            if permission != None and permission == UserPermission.SALES:
                Serializer = CRRegistrationSerializer
            else:
                Serializer = CRSignedRegistrationSerializer

        return Serializer(
            self,
            data=data,
            partial=True,
            context=context,
        )
