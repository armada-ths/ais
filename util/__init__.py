import os

from . import status

from rest_framework import serializers
from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.utils import timezone
from companies.models import CompanyContact, CompanyCustomerResponsible
from fair.models import Fair
from register.models import SignupLog
from exhibitors.models import Exhibitor
from people.models import Profile
from recruitment.models import RecruitmentApplication

from register.views import get_contract


is_dev = os.environ["DJANGO_SETTINGS_MODULE"] == "ais.local.settings"


def get_client_ip(request):
    return request.META["HTTP_REFERER"]


def is_react_dev_port(request):
    return urlparse(get_client_ip(request)).port == 5173  # `pnpm run dev`` in dashboard


class JSONError(BaseException):
    def __init__(self, status):
        self.status = status


def get_contract_signature(company, fair, type="COMPLETE"):
    signature = SignupLog.objects.filter(
        company=company, contract__fair=fair, contract__type=type
    ).first()

    if signature:
        contract = signature.contract
    else:
        contract = get_contract(company, fair, type)

    return (contract, signature)


def get_fair():
    return Fair.objects.filter(year=timezone.now().year).first()


def get_user(request):
    user = request.user
    if not user.is_authenticated:
        if is_dev and is_react_dev_port(request):
            user = User.objects.filter(email="dashboard@armada.nu").first()
            if user == None:
                raise Exception(
                    "No user with email dashboard@armada.nu. Please create one for local development."
                )
        else:
            return None

    return user


def get_company_contact(user):
    contact = CompanyContact.objects.filter(user=user).exclude(company=None).first()
    # if contact == None:
    #     raise status.USER_HAS_NO_COMPANY

    return contact


def get_exhibitor(company):
    return Exhibitor.objects.filter(fair=get_fair(), company=company).first()


def update_field(
    instance, validated_data, field: str, Serializer: serializers.Serializer
):
    item = validated_data.pop(field, None)
    if item != None:
        serializer = Serializer(getattr(instance, field), data=item, partial=True)

        if serializer.is_valid():
            serializer.save()


# Get the sales contacts for a company.
# If the company is an exhibitor for this fair, return the contact persons.
# If the company has a responsible, return that person.
# If no responsible, return the first person with a sales role.
def get_sales_contacts(fair, company, exhibitor):
    # Present the roles in this order if there is no sales responsible
    roles = ["Head of Sales", "Head of Business Relations", "Project Manager"]

    # Todo: test to see if exhibitor sort works
    if exhibitor is not None:
        contact_persons = exhibitor.contact_persons.all()
        if len(contact_persons) > 0:
            profiles = [
                Profile.objects.filter(user=user).first() for user in contact_persons
            ]
            profiles = [profile for profile in profiles if profile is not None]

            profile_roles = [
                RecruitmentApplication.objects.filter(
                    status="accepted",
                    user=profile.user,
                    recruitment_period__fair=fair,
                ).first()
                for profile in profiles
            ]

            # Sort such that the roles are in the order of the roles list
            # That is, OTs first, then Heads, then PM.
            profiles = sorted(
                zip(profiles, profile_roles),
                key=lambda x: (
                    -1 if x[1] is None else roles.index(x[1].delegated_role.name)
                ),
            )

            if len(profiles) > 0:
                return [profile[0] for profile in profiles]

    responsibles = CompanyCustomerResponsible.objects.filter(
        company=company, group__fair=fair, group__allow_responsibilities=True
    ).first()

    if responsibles is not None:
        users = responsibles.users.all()
        if len(users) > 0:
            profiles = [Profile.objects.filter(user=user).first() for user in users]
            return profiles

    for role in roles:
        for applicant in RecruitmentApplication.objects.filter(
            status="accepted",
            delegated_role__name=role,
            recruitment_period__fair=fair,
        ).all():
            profile = Profile.objects.filter(user=applicant.user).first()
            if profile is not None:
                return [profile]

    return []
