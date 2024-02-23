from util import get_contract_signature

from accounting.models import Product
from django.db.models import Q


def get_products(fair, company):
    contract, signature = get_contract_signature(company, fair, type="INITIAL")

    q = Q(exclusively_for=[])
    if signature == None:
        q |= Q(exclusively_for__contains=["ir-unsigned"])
    else:
        q |= Q(exclusively_for__contains=["ir-signed"])

    return Product.objects.filter(revenue__fair=fair).filter(q)
