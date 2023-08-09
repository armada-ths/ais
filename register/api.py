from enum import Enum

from rest_framework.parsers import JSONParser
from rest_framework import status, serializers

from drf_writable_nested import NestedUpdateMixin

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

from fair.models import Fair
from companies.models import CompanyContact
from exhibitors.models import Exhibitor
from register.models import SignupContract, SignupLog

from companies.serializers import CompanyCRSerializer

from register.views import get_contract


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContact
        fields = ("first_name", "last_name")


class FairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fair
        fields = ("name", "year", "description")


class SignupContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupContract
        fields = ("name", "contract")


class Registration:
    def __init__(self, type, deadline, company, contact, fair, contract):
        self.type = type
        self.deadline = deadline
        self.company = company
        self.contact = contact
        self.fair = fair
        self.contract = contract


class RegistrationSerializer(serializers.Serializer):
    type = serializers.StringRelatedField(read_only=True)
    deadline = serializers.DateTimeField(read_only=True)
    contact = ContactSerializer(read_only=True)
    fair = FairSerializer(read_only=True)
    contract = SignupContractSerializer(read_only=True)


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


class RegistrationState(Enum):
    BEFORE_IR = 1
    IR = 2
    AFTER_IR = 3
    CR = 4
    AFTER_CR = 5

    def get(fair: Fair):
        time = timezone.now()

        if time < fair.registration_start_date:
            return RegistrationState.BEFORE_IR
        elif time >= fair.registration_start_date and time < fair.registration_end_date:
            return RegistrationState.IR
        elif (
            time >= fair.registration_end_date
            and time < fair.complete_registration_start_date
        ):
            return RegistrationState.AFTER_IR
        elif (
            time >= fair.complete_registration_start_date
            and time < fair.complete_registration_close_date
        ):
            return RegistrationState.CR
        elif time >= fair.complete_registration_close_date:
            return RegistrationState.AFTER_CR


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


def index(request):
    """
    Root endpoint for all information regarding the current complete registration
    """

    user = request.user
    if not user.is_authenticated:
        # Todo: This is only for development, remove for prod!!
        user = User.objects.filter(email="dmu0817@3gamma.com").first()
        # return JsonResponse({"error": "not_authorized"}, safe=True, status=status.HTTP_401_UNAUTHORIZED)

    company_contacts = CompanyContact.objects.filter(user=user).exclude(company=None)

    if len(company_contacts) < 0:
        return JsonResponse(
            {"error": "user_has_no_company"},
            status=status.HTTP_404_NOT_FOUND,
        )

    contact = company_contacts.first()
    company = contact.company
    year = timezone.now().year
    fair = Fair.objects.filter(year=year).first()
    registration_period = RegistrationState.get(fair)

    not_implemented = JsonResponse(
        {"error": "not_implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED
    )

    # Todo 2023 (Didrik Munther): implement periods other than CR
    if registration_period == RegistrationState.BEFORE_IR:
        return not_implemented
    elif registration_period == RegistrationState.IR:
        return not_implemented
    elif registration_period == RegistrationState.AFTER_IR:
        return not_implemented
    elif registration_period == RegistrationState.CR:
        return handle_cr(request, company=company, fair=fair, contact=contact)
    elif registration_period == RegistrationState.AFTER_CR:
        return not_implemented
    else:
        return JsonResponse(
            {"error": "invalid_registration_period"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
