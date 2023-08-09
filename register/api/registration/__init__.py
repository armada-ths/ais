from django.http import JsonResponse
from django.utils import timezone

from fair.models import Fair
from companies.models import CompanyContact

from register.api import get_user, status
from register.api.registration.types import RegistrationState
from register.api.registration.cr import handle_cr

# Todo: remove this in prod
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def index(request):
    """
    Root endpoint for all information regarding the current complete registration
    """

    user = get_user(request)
    if user == None:
        return status.UNAUTHORIZED

    company_contacts = CompanyContact.objects.filter(user=user).exclude(company=None)

    if len(company_contacts) < 0:
        return status.USER_HAS_NO_COMPANY

    contact = company_contacts.first()
    company = contact.company
    year = timezone.now().year
    fair = Fair.objects.filter(year=year).first()
    registration_period = RegistrationState.get(fair)

    # Todo 2023 (Didrik Munther): implement periods other than CR
    if registration_period == RegistrationState.BEFORE_IR:
        return status.NOT_IMPLEMENTED
    elif registration_period == RegistrationState.IR:
        return status.NOT_IMPLEMENTED
    elif registration_period == RegistrationState.AFTER_IR:
        return status.NOT_IMPLEMENTED
    elif registration_period == RegistrationState.CR:
        return handle_cr(request, company=company, fair=fair, contact=contact)
    elif registration_period == RegistrationState.AFTER_CR:
        return status.NOT_IMPLEMENTED
    else:
        return status.INVALID_REGISTRATION_PERIOD