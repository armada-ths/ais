from rest_framework.parsers import JSONParser

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from register.api import get_user, status
from register.api.registration.types.registration import Registration
from register.api.registration.util import JSONError, get_contract_signature

from register.models import SignupLog
from accounting.models import Order

from register.views import send_CR_confirmation_email


def put_cr_registration(request, registration, purchasing_company):
    data = JSONParser().parse(request)
    serializer = registration.get_serializer(
        context={"user": get_user(request), "purchasing_company": purchasing_company},
        data=data,
    )

    if serializer.is_valid():
        serializer.update(registration, serializer.validated_data)
        return JsonResponse(serializer.data)

    return status.serializer_error(serializer.errors)


def get_registration(company, fair, contact, exhibitor):
    contract, signature = get_contract_signature(company, fair)
    orders = Order.objects.filter(purchasing_company=company)

    return Registration(
        company=company,
        contact=contact,
        contract=contract,
        signature=signature,
        fair=fair,
        exhibitor=exhibitor,
        orders=orders,
    )


def handle_cr(request, company, fair, contact, exhibitor):
    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    serializer = registration.get_serializer(context={"user": get_user(request)})

    if request.method == "GET":
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        return put_cr_registration(request, registration, company)
    else:
        return status.UNSUPPORTED_METHOD


@require_POST
def submit_cr(request, company, fair, contact, exhibitor):
    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    # Currently will not happen, because you can only
    # cal submit on your own company
    if registration.contact == None:
        return status.COMPANY_DOES_NOT_EXIST

    signature = registration.signature

    if signature != None:
        return status.EXHIBITOR_ALREADY_SIGNED

    signature = SignupLog.objects.create(
        company_contact=contact, contract=registration.contract, company=company
    )

    send_CR_confirmation_email(signature, registration.deadline)

    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    serializer = registration.get_serializer(context={"user": get_user(request)})

    return JsonResponse(serializer.data, safe=False)
