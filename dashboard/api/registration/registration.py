from django.views.decorators.csrf import csrf_exempt

from util import get_company_contact, get_exhibitor, get_fair, get_user, status

from companies.models import Company, CompanyContact
from fair.models import RegistrationState
from exhibitors.models import Exhibitor

from dashboard.api.registration.cr import handle_cr, submit_cr
from dashboard.api.registration.ir import handle_ir, submit_ir
from dashboard.api.registration.util import UserPermission


# This function will receive a GET or PUT and return
# a json structure of the registration state.
def render_company(request, company, contact, exhibitor):
    fair = get_fair()
    period = fair.get_period()

    if period == RegistrationState.BEFORE_IR:
        return status.IR_NOT_OPEN
    elif period == RegistrationState.IR:
        return handle_ir(request, company, fair, contact)
    elif period == RegistrationState.AFTER_IR:
        return handle_ir(request, company, fair, contact)
    elif period == RegistrationState.CR:
        return handle_cr(request, company, fair, contact, exhibitor)
    elif period == RegistrationState.AFTER_CR:
        return handle_cr(
            request, company, fair, contact, exhibitor
        )  # todo: temporary. What should really happen after CR?
    else:
        return status.INVALID_REGISTRATION_PERIOD


@csrf_exempt
def sign_ir(request):
    fair = get_fair()
    period = fair.get_period()
    if period != RegistrationState.IR:
        return status.INVALID_SUBMIT_PERIOD

    user = get_user(request)
    if user == None:
        return status.UNAUTHORIZED

    contact = get_company_contact(user)
    if contact == None:
        return status.USER_HAS_NO_COMPANY

    company = contact.company

    return submit_ir(request, company, fair, contact)


@csrf_exempt
def sign_cr(request):
    fair = get_fair()
    period = fair.get_period()
    if period != RegistrationState.CR:
        return status.INVALID_SUBMIT_PERIOD

    user = get_user(request)
    if user == None:
        return status.UNAUTHORIZED

    contact = get_company_contact(user)
    if contact == None:
        return status.USER_HAS_NO_COMPANY

    company = contact.company
    exhibitor = get_exhibitor(company)

    return submit_cr(request, company, fair, contact, exhibitor)


@csrf_exempt
def index(request):
    """
    Root endpoint for all information regarding the current complete registration
    """
    user = get_user(request)
    if user == None:
        return status.UNAUTHORIZED

    contact = get_company_contact(user)
    if contact == None:
        return status.USER_HAS_NO_COMPANY

    company = contact.company
    exhibitor = get_exhibitor(company)

    return render_company(request, company, contact, exhibitor)


@csrf_exempt
def get_company(request, company_pk):
    company = Company.objects.filter(pk=company_pk).first()
    if not company:
        return status.COMPANY_DOES_NOT_EXIST

    exhibitor = Exhibitor.objects.filter(fair=get_fair(), company=company).first()
    user = get_user(request)
    permission = UserPermission(user)
    user_is_contact_person = exhibitor and user in exhibitor.contact_persons.all()

    if permission == UserPermission.SALES or user_is_contact_person:
        contact = None
    else:
        contact = CompanyContact.objects.filter(user=user, company=company).first()

        if not contact:
            return status.UNAUTHORIZED

    return render_company(request, company, contact, exhibitor)
