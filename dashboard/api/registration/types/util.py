from rest_framework.fields import empty
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from dashboard.api.registration.types.cr import (
    CRRegistrationSerializer,
    CRSignedRegistrationSerializer,
)
from dashboard.api.registration.types.ir import IRRegistrationSerializer

from fair.models import RegistrationPeriod

from util import status, get_user
from util.permission import UserPermission


def get_serializer(request, registration, data=empty, context={}):
    context = {"request": request, **context}

    user = get_user(request)
    if user != None:
        permission = UserPermission(user)

    if registration.period in [
        RegistrationPeriod.BEFORE_IR,
        RegistrationPeriod.IR,
        RegistrationPeriod.BETWEEN_IR_AND_CR,
    ]:
        Serializer = IRRegistrationSerializer

    elif registration.period in [RegistrationPeriod.CR]:

        Serializer = CRRegistrationSerializer

        if registration.ir_signature == None:  # If IR has not been signed
            Serializer = IRRegistrationSerializer
        elif registration.cr_signature:
            # If user is sales, they may change anything he likes
            if permission != None and permission == UserPermission.SALES:
                Serializer = CRRegistrationSerializer
            else:
                Serializer = CRSignedRegistrationSerializer

    elif registration.period in [RegistrationPeriod.AFTER_CR]:
        Serializer = CRSignedRegistrationSerializer

    else:
        raise ValueError(
            f"This should not happen: {registration.period, registration.ir_signature, registration.cr_signature}"
        )

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
