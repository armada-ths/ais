from util import get_contract_signature

from accounting.models import Product
from django.db.models import Q


def get_products(fair, company):
    contract, signature = get_contract_signature(company, fair, type="INITIAL")
    if signature == None:
        return Product.objects.none()

    q = Q(exclusively_for=[])

    if signature.contract.is_timely:
        q |= Q(exclusively_for__contains=["ir-timely"])
    else:
        q |= Q(exclusively_for__contains=["ir-late"])

    return Product.objects.filter(revenue__fair=fair).filter(q)
