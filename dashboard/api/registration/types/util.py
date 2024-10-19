from rest_framework.fields import empty
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from dashboard.api.registration.types.cr import (
    CRRegistrationSerializer,
    CRSignedRegistrationSerializer,
)

from dashboard.api.registration.types.serializer import RegistrationSerializer
from fair.models import RegistrationPeriod

from util import status, get_user
from util.permission import UserPermission


def get_serializer(request, registration, data=empty, context={}):
    context = {"request": request, **context}

    user = get_user(request)
    if user != None:
        permission = UserPermission(user)

    if (
        registration.period
        in [
            RegistrationPeriod.BEFORE_IR,
            RegistrationPeriod.IR,
            RegistrationPeriod.BETWEEN_IR_AND_CR,
        ]
        or registration.ir_signature is None
    ):
        Serializer = RegistrationSerializer
    elif registration.period in [RegistrationPeriod.CR]:
        # If user is sales, they may change anything he likes
        if permission == UserPermission.SALES or registration.cr_signature is None:
            Serializer = CRRegistrationSerializer
        else:
            Serializer = CRSignedRegistrationSerializer

    elif registration.period in [
        RegistrationPeriod.AFTER_CR,
        RegistrationPeriod.FAIR,
        RegistrationPeriod.AFTER_FAIR,
    ]:
        Serializer = CRSignedRegistrationSerializer

    else:
        raise ValueError(f"Unhandled registration period: {registration.period}")

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
