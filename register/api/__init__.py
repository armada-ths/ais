from rest_framework import status

from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User

from fair.models import Fair
from companies.models import CompanyContact

from register.api.registration.types import RegistrationState
from register.api.registration.cr import handle_cr


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
