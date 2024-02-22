from ais.common import settings
from dashboard.api.registration.types.registration import get_registration
from util import JSONError, get_user, status

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from dashboard.api.registration.types.util import get_serializer, put_registration

from register.models import SignupLog
from accounting.models import Order

from util.email import send_mail
from util.ip import get_client_ip


def handle_cr(request, company, fair, contact, exhibitor):
    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    serializer = get_serializer(request, registration)

    if request.method == "GET":
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        return put_registration(request, registration, company)
    else:
        return status.UNSUPPORTED_METHOD


@require_POST
def submit_cr(request, company, fair, contact, exhibitor):
    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    # Currently will not happen, because you can only
    # call submit on your own company
    if registration.contact == None:
        return status.COMPANY_DOES_NOT_EXIST

    signature = registration.cr_signature

    if signature != None:
        return status.EXHIBITOR_ALREADY_SIGNED

    signature = SignupLog.objects.create(
        company_contact=contact,
        contract=registration.cr_contract,
        company=company,
        ip_address=get_client_ip(request),
    )

    # Add package products
    package_products = Order.objects.filter(
        purchasing_company=company,
        product__revenue__fair=fair,
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

    # Untested
    # Todo: Add packages to email
    send_mail(
        request,
        template="register/email/cr_complete.html",
        context={
            "company": company,
            "fair": fair,
            "signature": signature,
            "deadline": registration.deadline,
        },
        subject="Final registration received!",
        to=[signature.company_contact.email_address],
        file_paths=[settings.MEDIA_ROOT + signature.contract.contract.url[6:]],
    )

    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    serializer = get_serializer(request, registration)

    return JsonResponse(serializer.data, safe=False)
