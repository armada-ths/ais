from django.shortcuts import get_object_or_404


from fair.serializers import lunch_ticket, banquet_participant
from fair.models import Fair, OrganizationGroup, LunchTicket

from banquet.models import Banquet, Participant # This could be moved to a 'banquet.selectors' file
from recruitment.models import RecruitmentApplication # This could be moved to a 'recruitment.selectors' file


def get_fair(year):
    return  get_object_or_404(Fair, year=year)


def get_lunch_tickets_by_fair(fair):
    return LunchTicket.objects.select_related('user').select_related('company').select_related('day').select_related(
            'time').prefetch_related('dietary_restrictions').filter(fair=fair)

def get_filtered_lunch_tickets(fair):
    lunch_tickets = get_lunch_tickets_by_fair(fair=fair)
    filtered_lunch_tickets = []


        for lunchticket in lunchtickets:
            if len(form.cleaned_data['used_statuses']) > 0:
                found = False

                for s in form.cleaned_data['used_statuses']:
                    if s == 'USED' and lunchticket.used:
                        found = True
                        break

                    if s == 'NOT_USED' and not lunchticket.used:
                        found = True
                        break

                if not found: continue

            if len(form.cleaned_data['types']) > 0:
                found = False

                for t in form.cleaned_data['types']:
                    if t == 'STUDENT' and lunchticket.company is None:
                        found = True
                        break

                    if t == 'COMPANY' and lunchticket.company is not None:
                        found = True
                        break

                if not found: continue

            if len(form.cleaned_data['sent_statuses']) > 0:
                found = False

                for t in form.cleaned_data['sent_statuses']:
                    if t == 'SENT' and lunchticket.sent:
                        found = True
                        break

                    if t == 'NOT_SENT' and not lunchticket.sent:
                        found = True
                        break

                if not found: continue

            if len(form.cleaned_data['days']) > 0:
                found = False

                for d in form.cleaned_data['days']:
                    if lunchticket.day == d:
                        found = True
                        break

                if not found: continue

            lunchtickets_filtered.append({
                't': lunchticket,
                'drl': []
            })


def get_users_from_organization_groups(fair):
    organization_groups = OrganizationGroup.objects.filter(fair=fair)
    users = []
    for organization_group in organizations_groups:
        applicant_users = [applicant.user for applicant in RecruitmentApplication.objects.select_related('user')
                .filter(
                    delegated_role__organization_group=organization_group, 
                    status='accepted', 
                    recruitment_period__fair=fair)
                .order_by('user__first_name', 'user__last_name')]
        users.append([organization_group.name, [(user.pk, user.get_full_name()) for user in applicant_users]])

    return users


def get_lunch_tickets(fair, user):
    return LunchTicket.objects.filter(fair=fair, user=user)


def get_serialized_lunch_tickets(fair, user):
    return [lunch_ticket(lunch_ticket=lunch_ticket) for lunch_ticket in get_lunch_tickets(fair=fair, user=user)]


def get_lunch_ticket(token):
    return  get_object_or_404(LunchTicket, fair__current=True, token=token)


def get_banquet_particiapnt(fair, user):
    banquet = Banquet.objects.filter(fair=fair).first()
    banquet_participant = Participant.objects.filter(user=user, banquet=banquet).first()
    return banquet_participant(banquet_participant) if banquet_participant else None
