from util import JSONError, get_user, status

from rest_framework.parsers import JSONParser

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from register.api.registration.types.registration import Registration
from register.api.registration.types.util import get_serializer

from register.models import SignupLog
from accounting.models import Order

from register.views import send_CR_confirmation_email


def put_cr_registration(request, registration, purchasing_company):
    data = JSONParser().parse(request)
    serializer = get_serializer(
        registration,
        context={"user": get_user(request), "purchasing_company": purchasing_company},
        data=data,
    )

    if serializer.is_valid():
        serializer.update(registration, serializer.validated_data)
        return JsonResponse(serializer.data)

    return status.serializer_error(serializer.errors)


def get_registration(company, fair, contact, exhibitor):
    orders = Order.objects.filter(
        purchasing_company=company, product__revenue__fair=fair
    )

    return Registration(
        company=company,
        contact=contact,
        fair=fair,
        exhibitor=exhibitor,
        orders=orders,
    )


def handle_cr(request, company, fair, contact, exhibitor):
    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    serializer = get_serializer(registration, context={"user": get_user(request)})

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
    # call submit on your own company
    if registration.contact == None:
        return status.COMPANY_DOES_NOT_EXIST

    signature = registration.signature

    if signature != None:
        return status.EXHIBITOR_ALREADY_SIGNED

    signature = SignupLog.objects.create(
        company_contact=contact, contract=registration.contract, company=company
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

    try:
        send_CR_confirmation_email(signature, registration.deadline)
    except:
        pass

    try:
        registration = get_registration(company, fair, contact, exhibitor)
    except JSONError as error:
        return error.status

    serializer = get_serializer(registration, context={"user": get_user(request)})

    return JsonResponse(serializer.data, safe=False)
