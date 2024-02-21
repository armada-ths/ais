from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings

from util import JSONError, get_user, status
from util.email import send_mail

from register.api.registration.types.registration import get_registration
from register.api.registration.types.util import get_serializer, put_registration

from register.models import SignupLog


def handle_ir(request, company, fair, contact):
    try:
        registration = get_registration(company, fair, contact, None)
    except JSONError as error:
        return error.status

    serializer = get_serializer(registration, context={"user": get_user(request)})

    if request.method == "GET":
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        return put_registration(request, registration, company)
    else:
        return status.UNSUPPORTED_METHOD


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
        company_contact=contact, contract=registration.ir_contract, company=company
    )

    send_mail(
        request,
        template="register/email/ir_complete.html",
        context={"company": company, "fair": fair, "signature": signature},
        subject="Initial registration received!",
        to=[signature.company_contact.email_address],
        file_paths=[settings.MEDIA_ROOT + signature.contract.contract.url[6:]],
    )

    try:
        registration = get_registration(company, fair, contact, None)
    except JSONError as error:
        return error.status

    serializer = get_serializer(registration, context={"user": get_user(request)})

    return JsonResponse(serializer.data, safe=False)
