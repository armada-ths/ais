from dashboard.api.registration.email import (
    send_cr_confirmation_email,
    send_ir_confirmation_email,
)
from dashboard.api.registration.types.registration import get_registration
from exhibitors.models import Exhibitor
from util import JSONError, get_contract_signature, get_exhibitor, status

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from dashboard.api.registration.types.util import get_serializer, put_registration

from register.models import SignupLog
from accounting.models import Order

from util.ip import get_client_ip


def ensure_exhibitor_exists_after_ir_signup(fair, company):
    _ir_contract, ir_signature = get_contract_signature(company, fair, "INITIAL")
    exhibitor = Exhibitor.objects.filter(fair=fair, company=company).first()

    if ir_signature != None and exhibitor == None:
        Exhibitor.objects.create(fair=fair, company=company)


def handle_response(request, company, fair, contact, exhibitor):
    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    serializer = get_serializer(request, registration)

    print(order_is_allowed(fair, company))

    if request.method == "GET":
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        return put_registration(request, registration, company)
    else:
        return status.UNSUPPORTED_METHOD


def order_is_allowed(fair, company):
    orders = Order.objects.filter(
        purchasing_company=company,
        product__revenue__fair=fair,
    )

    package = orders.filter(product__category__name="Package").first()
    if package is None:
        return False

    return True


def handle_submitted_order(fair, company):
    orders = Order.objects.filter(
        purchasing_company=company,
        product__revenue__fair=fair,
    )

    # Add package products
    package_products = orders.filter(
        product__category__name="Package",
    )
    for package in package_products:
        for child in package.product.child_products.all():
            Order.objects.create(
                purchasing_company=company,
                product=child.child_product,
                quantity=child.quantity,
                unit_price=0,  # A package product is free
            )


@require_POST
def submit_cr(request, company, fair, contact, exhibitor):
    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    if registration.contact == None:
        return status.COMPANY_DOES_NOT_EXIST

    if registration.cr_signature != None:
        return status.EXHIBITOR_ALREADY_SIGNED

    if registration.ir_signature is None:
        return status.COMPANY_NOT_SIGNED_IR

    if not order_is_allowed(fair, company):
        return status.ORDER_NOT_ALLOWED

    signature = SignupLog.objects.create(
        company_contact=contact,
        contract=registration.cr_contract,
        company=company,
        ip_address=get_client_ip(request),
    )

    handle_submitted_order(fair, company)
    send_cr_confirmation_email(request, fair, company, exhibitor, signature)

    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    serializer = get_serializer(request, registration)

    return JsonResponse(serializer.data, safe=False)


@require_POST
def submit_ir(request, company, fair, contact):
    try:
        registration = get_registration(company, fair, contact, None)
    except JSONError as error:
        return error.status

    if registration.contact == None:
        return status.COMPANY_DOES_NOT_EXIST

    signature = registration.ir_signature
    if signature != None:
        return status.COMPANY_ALREADY_SIGNED

    signature = SignupLog.objects.create(
        company_contact=contact,
        contract=registration.ir_contract,
        company=company,
        ip_address=get_client_ip(request),
    )

    ensure_exhibitor_exists_after_ir_signup(fair, company)
    send_ir_confirmation_email(request, fair, signature, company)

    exhibitor = get_exhibitor(company)

    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    serializer = get_serializer(request, registration)

    return JsonResponse(serializer.data, safe=False)
