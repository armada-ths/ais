from rest_framework.parsers import JSONParser

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from register.api import status
from register.api.registration.types import (
    Registration,
    get_contract_signature,
)

from register.models import SignupLog
from accounting.models import Order


def put_cr_registration(request, registration, purchasing_company):
    data = JSONParser().parse(request)
    serializer = registration.get_serializer(
        data, context={"purchasing_company": purchasing_company}
    )

    if serializer.is_valid():
        serializer.update(registration, serializer.validated_data)
        return JsonResponse(serializer.data)

    return status.serializer_error(serializer.errors)


def get_registration(company, fair, contact, exhibitor):
    contract, signature = get_contract_signature(company, fair)

    if exhibitor == None:
        if signature == None:
            return status.USER_DID_NOT_SIGN
        else:
            return status.USER_IS_NOT_EXHIBITOR

    orders = Order.objects.filter(purchasing_company=company)

    return Registration(
        company=company,
        contact=contact,
        fair=fair,
        exhibitor=exhibitor,
        contract=contract,
        orders=orders,
    )


def handle_cr(request, company, fair, contact, exhibitor):
    registration = get_registration(company, fair, contact, exhibitor)
    serializer = registration.get_serializer()

    if request.method == "GET":
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        return put_cr_registration(request, registration, company)
    else:
        return status.UNSUPPORTED_METHOD


@require_POST
def submit_cr(request, company, fair, contact, exhibitor):
    registration = get_registration(company, fair, contact, exhibitor)
    _, signature = get_contract_signature(company, fair)

    if signature != None:
        return status.EXHIBITOR_ALREADY_SIGNED

    # if not form_final_submission.is_valid():
    #     return error

    signature = SignupLog.objects.create(
        company_contact=contact, contract=registration.contract, company=company
    )

    # deadline = (
    #     exhibitor.deadline_complete_registration
    #     or fair.complete_registration_close_date
    # )
    # send_CR_confirmation_email(signature, deadline)

    registration = get_registration(company, fair, contact, exhibitor)

    try:
        serializer = registration.get_serializer()
    except:
        return

    return JsonResponse(serializer.data, safe=False)
