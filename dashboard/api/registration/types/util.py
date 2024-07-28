from rest_framework.fields import empty
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from dashboard.api.registration.types.cr import (
    CRRegistrationSerializer,
    CRSignedRegistrationSerializer,
)
from dashboard.api.registration.types.ir import IRRegistrationSerializer
from dashboard.api.registration.types.registration import RegistrationType

from util import status, get_user
from util.permission import UserPermission


def get_serializer(request, registration, data=empty, context={}):
    context = {"request": request, **context}

    user = get_user(request)
    if user != None:
        permission = UserPermission(user)

    # IR
    if registration.type == RegistrationType.BeforeInitialRegistration:
        Serializer = IRRegistrationSerializer
    elif registration.type == RegistrationType.InitialRegistration:
        Serializer = IRRegistrationSerializer
    elif registration.type == RegistrationType.InitialRegistrationSigned:
        Serializer = IRRegistrationSerializer
    elif registration.type == RegistrationType.AfterInitialRegistration:
        Serializer = IRRegistrationSerializer
    elif registration.type == RegistrationType.AfterInitialRegistrationSigned:
        Serializer = IRRegistrationSerializer

    # CR
    elif registration.type == RegistrationType.BeforeCompleteRegistrationIRSigned:
        Serializer = CRRegistrationSerializer
    elif registration.type == RegistrationType.BeforeCompleteRegistrationIRUnsigned:
        Serializer = CRRegistrationSerializer
    elif registration.type == RegistrationType.CompleteRegistrationIRSigned:
        Serializer = CRRegistrationSerializer
    elif registration.type == RegistrationType.CompleteRegistrationIRUnsigned:
        Serializer = CRRegistrationSerializer
    elif registration.type == RegistrationType.CompleteRegistrationSigned:
        # If user is sales, they may change anything he likes
        if permission != None and permission == UserPermission.SALES:
            Serializer = CRRegistrationSerializer
        else:
            Serializer = CRSignedRegistrationSerializer
    elif (
        registration.type == RegistrationType.AfterInitialRegistrationAcceptanceAccepted
        or registration.type
        == RegistrationType.AfterInitialRegistrationAcceptanceRejected
        or registration.type
        == RegistrationType.AfterInitialRegistrationAcceptanceTentative
    ):
        Serializer = CRRegistrationSerializer
    elif registration.type == RegistrationType.AfterCompleteRegistration:
        Serializer = CRSignedRegistrationSerializer
    elif registration.type == RegistrationType.AfterCompleteRegistrationSigned:
        Serializer = CRSignedRegistrationSerializer
    else:
        raise ValueError(f"Unknown registration type: {registration.type}")

    return Serializer(
        registration,
        data=data,
        partial=True,
        context=context,
    )


def put_registration(request, registration, purchasing_company):
    data = JSONParser().parse(request)
    serializer = get_serializer(
        request,
        registration,
        data=data,
        context={"purchasing_company": purchasing_company},
    )

    if serializer.is_valid():
        serializer.update(registration, serializer.validated_data)
        return JsonResponse(serializer.data)

    return status.serializer_error(serializer.errors)
