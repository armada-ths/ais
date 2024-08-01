from rest_framework import status

from django.http import JsonResponse


def serializer_error(errors):
    return JsonResponse(errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


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
IR_NOT_OPEN = JsonResponse(
    {
        "error": "ir_not_open",
        "message": "There is no active initial registration contract",
    },
    status=status.HTTP_403_FORBIDDEN,
)
CR_NOT_OPEN = JsonResponse(
    {
        "error": "cr_not_open",
        "message": "There is no active final registration contract",
    },
    status=status.HTTP_403_FORBIDDEN,
)
USER_HAS_NO_COMPANY = JsonResponse(
    {"error": "user_has_no_company"},
    status=status.HTTP_404_NOT_FOUND,
)
COMPANY_ALREADY_SIGNED = JsonResponse(
    {"error": "company_already_signed", "message": "Company has already signed IR"},
    status=status.HTTP_403_FORBIDDEN,
)
COMPANY_NOT_SIGNED_IR = JsonResponse(
    {"error": "company_did_not_sign_ir", "message": "Company has not signed IR"},
    status=status.HTTP_403_FORBIDDEN,
)
COMPANY_NOT_ACCEPTED = JsonResponse(
    {"error": "company_not_accepted", "message": "Company has not been accepted"},
    status=status.HTTP_403_FORBIDDEN,
)
EXHIBITOR_ALREADY_SIGNED = JsonResponse(
    {"error": "exhibitor_already_signed", "message": "Exhibitor has already signed CR"},
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

COMPANY_TYPE_DOES_NOT_EXIST = JsonResponse(
    {
        "error": "company_type_does_not_exist",
        "message": "Or there is no default company type",
    },
    status=status.HTTP_404_NOT_FOUND,
)
USER_ALREADY_EXISTS = JsonResponse(
    {"error": "user_already_exists"},
    status=status.HTTP_400_BAD_REQUEST,
)
