from rest_framework.parsers import JSONParser

from django.http import JsonResponse
from accounting.models import Order
from register.api import status

from register.api.registration.types import Registration, RegistrationSerializer
from register.api.registration.serializer import CompanyCRSerializer

from exhibitors.models import Exhibitor
from register.models import SignupLog

from register.views import get_contract


class RegistrationCRSerializer(RegistrationSerializer):
    company = CompanyCRSerializer()

    def update(self, instance, validated_data):
        company = validated_data.pop("company", None)
        if company:
            company_serializer = CompanyCRSerializer(
                instance.company, data=company, partial=True
            )
            if company_serializer.is_valid():
                company_serializer.save()

        return instance


def put_cr_registration(request, registration):
    data = JSONParser().parse(request)
    serializer = RegistrationCRSerializer(registration, data=data, partial=True)

    if serializer.is_valid():
        serializer.update(registration, serializer.validated_data)
        return JsonResponse(serializer.data)

    return status.serializer_error(serializer.errors)


def handle_cr(request, company, fair, contact):
    signature = SignupLog.objects.filter(
        company=company, contract__fair=fair, contract__type="COMPLETE"
    ).first()

    if signature:
        contract = signature.contract
    else:
        contract = get_contract(company, fair, "COMPLETE")

    exhibitor = Exhibitor.objects.filter(fair=fair, company=company).first()
    if exhibitor == None:
        return status.USER_IS_NOT_EXHIBITOR

    deadline = (
        exhibitor.deadline_complete_registration
        or fair.complete_registration_close_date
    )

    orders = Order.objects.filter(purchasing_company=company)

    registration = Registration(
        type="complete_registration",
        deadline=deadline,
        company=company,
        contact=contact,
        fair=fair,
        contract=contract,
        orders=orders,
    )

    if request.method == "GET":
        return JsonResponse(RegistrationCRSerializer(registration).data, safe=False)
    elif request.method == "PUT":
        return put_cr_registration(request, registration)
    else:
        return status.UNSUPPORTED_METHOD
