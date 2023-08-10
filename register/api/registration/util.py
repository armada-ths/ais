from enum import Enum

from django.utils import timezone

from fair.models import Fair
from register.models import SignupLog

from register.views import get_contract


class UserPermission(Enum):
    COMPANY_CONTACT = 0
    SALES = 1

    @classmethod
    def _missing_(cls, user):
        is_sales = user.has_perm("companies.base") or user.has_perm(
            "exhibitors.view_all"
        )

        if is_sales:
            return cls(UserPermission.SALES)
        else:
            return cls(UserPermission.COMPANY_CONTACT)


def get_fair():
    return Fair.objects.filter(year=timezone.now().year).first()


def get_contract_signature(company, fair):
    signature = SignupLog.objects.filter(
        company=company, contract__fair=fair, contract__type="COMPLETE"
    ).first()

    if signature:
        contract = signature.contract
    else:
        contract = get_contract(company, fair, "COMPLETE")

    return (contract, signature)
