import datetime
from ais.common import settings
from dashboard.api.registration.types.registration import get_registration
from exhibitors.models import Exhibitor
from util import JSONError, get_contract_signature, get_exhibitor, status

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from dashboard.api.registration.types.util import get_serializer, put_registration

from register.models import SignupLog
from accounting.models import Order

from util.email import send_mail
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

    if registration.cr_signature != None:
        return status.EXHIBITOR_ALREADY_SIGNED

    if registration.ir_signature is None:
        return status.COMPANY_NOT_SIGNED_IR

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
            "deadline": exhibitor.deadline_complete_registration
            or fair.complete_registration_close_date,
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


def send_ir_confirmation_email(
    request,
    fair,
    signature,
    company,
    # How many days the company has to change their initial registration application after signing the contract
    ir_application_change_allowed_time=14,
    # How many days after the initial registration end date the company will receive a confirmation email
    ir_application_review_time=14,
):
    # The deadline for the company to change their initial registration application
    # either x days after signature, or the registration end date, whichever comes last.
    ir_application_change_deadline = max(
        [
            signature.timestamp
            + datetime.timedelta(days=ir_application_change_allowed_time),
            fair.registration_end_date,
        ]
    )

    # The latest date the company will receive a confirmation email
    ir_application_review_date = fair.registration_end_date + datetime.timedelta(
        days=ir_application_review_time
    )

    send_mail(
        request,
        template="register/email/ir_complete.html",
        context={
            "company": company,
            "fair": fair,
            "signature": signature,
            "ir_application_change_deadline": ir_application_change_deadline,
            "ir_application_review_date": ir_application_review_date,
            "support_email": "sales@armada.nu",
        },
        subject="Initial registration received!",
        to=[signature.company_contact.email_address],
        file_paths=[settings.MEDIA_ROOT + signature.contract.contract.url[6:]],
    )


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
