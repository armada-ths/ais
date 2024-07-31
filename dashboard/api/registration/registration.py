from django.views.decorators.csrf import csrf_exempt

from util import (
    get_company_contact,
    get_contract_signature,
    get_exhibitor,
    get_fair,
    get_user,
    status,
)
from util.permission import UserPermission

from companies.models import Company, CompanyContact
from fair.models import RegistrationPeriod
from exhibitors.models import Exhibitor

from dashboard.api.registration.response import handle_response, submit_cr, submit_ir


# (Didrik 2024)
# During the 2024 fair, we decided to add a IR-bypass system,
# allowing companies to sign up for IR after the official IR period had ended.
# We do this by creating an exhibitor after the company has signed the IR contract.
# This function handles the creation of exhibitors for companies which had signed
# IR before this change was implemented. It will not be needed in the future,
# but also does not cause any harm to keep.
def ensure_exhibitor_exists_after_ir_signup(fair, company):
    _ir_contract, ir_signature = get_contract_signature(company, fair, "INITIAL")
    exhibitor = Exhibitor.objects.filter(fair=fair, company=company).first()

    if ir_signature != None and exhibitor == None:
        Exhibitor.objects.create(fair=fair, company=company)


# This function will receive a GET or PUT and return
# a json structure of the registration state.
def render_company(request, company, contact, exhibitor):
    fair = get_fair()

    ensure_exhibitor_exists_after_ir_signup(fair, company)

    return handle_response(request, company, fair, contact, exhibitor)


@csrf_exempt
def sign_ir(request):
    fair = get_fair()
    period = fair.get_period()
    if period != RegistrationPeriod.IR:
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
    if period != RegistrationPeriod.CR:
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
