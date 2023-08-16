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
INVALID_SUBMIT_PERIOD = JsonResponse(
    {"error": "invalid_submit_period", "message": "Did you already submit?"},
    status=status.HTTP_403_FORBIDDEN,
)
INVALID_REGISTRATION_PERIOD = JsonResponse(
    {"error": "invalid_registration_period"},
    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
)
USER_HAS_NO_COMPANY = JsonResponse(
    {"error": "user_has_no_company"},
    status=status.HTTP_404_NOT_FOUND,
)
EXHIBITOR_ALREADY_SIGNED = JsonResponse(
    {"error": "exhibitor_already_signed"},
    status=status.HTTP_403_FORBIDDEN,
)
COMPANY_DOES_NOT_EXIST = JsonResponse(
    {"error": "company_does_not_exist"},
    status=status.HTTP_404_NOT_FOUND,
)
USER_DID_NOT_SIGN_IR = JsonResponse(
    {"error": "user_did_not_sign_ir"},
    status=status.HTTP_401_UNAUTHORIZED,
)
USER_IS_NOT_EXHIBITOR = JsonResponse(
    {"error": "user_is_not_exhibitor"},
    status=status.HTTP_401_UNAUTHORIZED,
)
USER_NOT_ALLOWED_TO_SUBMIT = JsonResponse(
    {
        "error": "user_not_allowed_to_submit",
        "message": "You are not a contact person for this company",
    },
    status=status.HTTP_401_UNAUTHORIZED,
)
UNSUPPORTED_METHOD = JsonResponse(
    {"error": "unsupported_method"},
    status=status.HTTP_405_METHOD_NOT_ALLOWED,
)
