from rest_framework import status

from django.http import JsonResponse


def serializer_error(errors):
    return JsonResponse(errors, status=status.HTTP_400_BAD_REQUEST)


UNAUTHORIZED = JsonResponse(
    {"error": "not_authorized"}, status=status.HTTP_401_UNAUTHORIZED
)
NOT_IMPLEMENTED = JsonResponse(
    {"error": "not_implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED
)
INVALID_REGISTRATION_PERIOD = JsonResponse(
    {"error": "invalid_registration_period"},
    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
)
USER_HAS_NO_COMPANY = JsonResponse(
    {"error": "user_has_no_company"},
    status=status.HTTP_404_NOT_FOUND,
)
USER_IS_NOT_EXHIBITOR = JsonResponse(
    {"error": "user_is_not_exhibitor"},
    status=status.HTTP_401_UNAUTHORIZED,
)
UNSUPPORTED_METHOD = JsonResponse(
    {"error": "unsupported_method"},
    status=status.HTTP_405_METHOD_NOT_ALLOWED,
)
