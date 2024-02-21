from rest_framework.fields import empty
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from register.api.registration.types.cr import (
    CRRegistrationSerializer,
    CRSignedRegistrationSerializer,
)
from register.api.registration.types.ir import IRRegistrationSerializer
from register.api.registration.types.registration import RegistrationType
from register.api.registration.util import (
    UserPermission,
)

from util import status, get_user


def get_serializer(registration, data=empty, context={}):
    user = context["user"]
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
        registration,
        context={"user": get_user(request), "purchasing_company": purchasing_company},
        data=data,
    )

    if serializer.is_valid():
        serializer.update(registration, serializer.validated_data)
        return JsonResponse(serializer.data)

    return status.serializer_error(serializer.errors)
