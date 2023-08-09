from rest_framework import status
from rest_framework.parsers import JSONParser

from django.http import JsonResponse

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

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return JsonResponse(
            {"error": "user_is_not_exhibitor"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    deadline = (
        exhibitor.deadline_complete_registration
        or fair.complete_registration_close_date
    )

    registration = Registration(
        type="complete_registration",
        deadline=deadline,
        company=company,
        contact=contact,
        fair=fair,
        contract=contract,
    )

    if request.method == "GET":
        return JsonResponse(RegistrationCRSerializer(registration).data, safe=False)
    elif request.method == "PUT":
        return put_cr_registration(request, registration)
    else:
        return JsonResponse(
            {"error": "unsupported_method"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
