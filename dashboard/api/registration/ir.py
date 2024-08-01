import datetime

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings

from util import JSONError, get_user, status
from util.email import send_mail
from util.ip import get_client_ip

from dashboard.api.registration.types.registration import get_registration
from dashboard.api.registration.types.util import get_serializer, put_registration

from register.models import SignupLog


def handle_ir(request, company, fair, contact, exhibitor):
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

    send_ir_confirmation_email(request, fair, signature, company)

    try:
        registration = get_registration(company, fair, contact, None)
    except JSONError as error:
        return error.status

    serializer = get_serializer(request, registration)

    return JsonResponse(serializer.data, safe=False)
