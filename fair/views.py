import json

from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from banquet.models import Participant, Banquet
from companies.models import CompanyContact
from events.models import Event
from fair import serializers
from recruitment.models import RecruitmentApplication
from recruitment.models import RecruitmentPeriod, Role

from .forms import LunchTicketForm, LunchTicketSearchForm
from .models import Fair, LunchTicket, LunchTicketSend
from .models import FairDay, OrganizationGroup


def login_redirect(request):
    next = request.GET.get("next")
    if next and next[-1] == "/":
        next = next[:-1]

    print(request.user)
    if request.user.is_authenticated:
        contact = CompanyContact.objects.filter(user=request.user).first()
        fair = Fair.objects.filter(current=True).first()
        if fair is None:
            fair = Fair.objects.filter.first()
        year = fair.year

        if contact is not None:
            return redirect("anmalan:choose_company")

        return redirect("fair:home", year)

    return render(request, "login.html", {"next": next})


def index(request, year=None):
    fair = Fair.objects.filter(year=year).first()
    if fair is None:
        fair = Fair.objects.filter(current=True).first()
        return redirect("fair:home", fair.year)

    if not request.user.is_authenticated:
        return render(request, "login.html", {"next": next, "fair": fair})

    if request.user.has_perm("events.base"):
        events = Event.objects.filter(fair=fair).annotate(
            num_participants=Count("participant")
        )
    else:
        events = Event.objects.filter(fair=fair, published=True)

    recruitment_period = RecruitmentPeriod.objects.filter(fair=fair).order_by(
        "-start_date"
    )

    return render(
        request,
        "fair/home.html",
        {
            "recruitment": {
                "recruitment_periods": recruitment_period,
            },
            "events": events,
            "fair": fair,
        },
    )


@permission_required("fair.lunchtickets")
def lunchtickets(request, year):
    fair = get_object_or_404(Fair, year=year)

    form = LunchTicketSearchForm(request.POST or None)

    form.fields["days"].queryset = FairDay.objects.filter(fair=fair)

    if request.POST and form.is_valid():
        lunchtickets = (
            LunchTicket.objects.select_related("user")
            .select_related("company")
            .select_related("day")
            .select_related("time")
            .prefetch_related("dietary_restrictions")
            .filter(fair=fair)
        )
        lunchtickets_filtered = []

        for lunchticket in lunchtickets:
            if len(form.cleaned_data["used_statuses"]) > 0:
                found = False

                for s in form.cleaned_data["used_statuses"]:
                    if s == "USED" and lunchticket.used:
                        found = True
                        break

                    if s == "NOT_USED" and not lunchticket.used:
                        found = True
                        break

                if not found:
                    continue

            if len(form.cleaned_data["types"]) > 0:
                found = False

                for t in form.cleaned_data["types"]:
                    if t == "STUDENT" and lunchticket.company is None:
                        found = True
                        break

                    if t == "COMPANY" and lunchticket.company is not None:
                        found = True
                        break

                if not found:
                    continue

            if len(form.cleaned_data["sent_statuses"]) > 0:
                found = False

                for t in form.cleaned_data["sent_statuses"]:
                    if t == "SENT" and lunchticket.sent:
                        found = True
                        break

                    if t == "NOT_SENT" and not lunchticket.sent:
                        found = True
                        break

                if not found:
                    continue

            if len(form.cleaned_data["days"]) > 0:
                found = False

                for d in form.cleaned_data["days"]:
                    if lunchticket.day == d:
                        found = True
                        break

                if not found:
                    continue

            lunchtickets_filtered.append({"t": lunchticket, "drl": []})

        dietary_restrictions_all = {}

        if form.cleaned_data["include_dietary_restrictions"]:
            for lunchticket in lunchtickets_filtered:
                for dietary_restriction in lunchticket["t"].dietary_restrictions.all():
                    if dietary_restriction in dietary_restrictions_all:
                        dietary_restrictions_all[dietary_restriction] += 1
                    else:
                        dietary_restrictions_all[dietary_restriction] = 1

            for lunchticket in lunchtickets_filtered:
                lunchticket["drl"] = [
                    (
                        True
                        if dietary_restriction
                        in lunchticket["t"].dietary_restrictions.all()
                        else False
                    )
                    for dietary_restriction in dietary_restrictions_all
                ]

    else:
        lunchtickets_filtered = []
        dietary_restrictions_all = {}

    return render(
        request,
        "fair/lunchtickets.html",
        {
            "fair": fair,
            "my_lunchtickets": LunchTicket.objects.filter(fair=fair, user=request.user),
            "form": form,
            "has_searched": request.POST and form.is_valid(),
            "lunchtickets": lunchtickets_filtered,
            "dietary_restrictions": [
                {"name": x, "count": dietary_restrictions_all[x]}
                for x in dietary_restrictions_all
            ],
        },
    )


@permission_required("fair.lunchtickets")
def lunchticket(request, year, token):
    fair = get_object_or_404(Fair, year=year)
    lunch_ticket = get_object_or_404(LunchTicket, fair=fair, token=token)

    if request.user != lunch_ticket.user and not request.user.has_perm(
        "fair.lunchtickets"
    ):
        return HttpResponseForbidden()

    if request.user.has_perm("fair.lunchtickets"):
        form = LunchTicketForm(request.POST or None, instance=lunch_ticket)

        if request.POST and form.is_valid():
            form.save()

    else:
        form = None

    return render(
        request,
        "fair/lunchticket.html",
        {
            "fair": fair,
            "lunch_ticket": lunch_ticket,
            "form": form,
            "sends": LunchTicketSend.objects.filter(lunch_ticket=lunch_ticket),
        },
    )


@permission_required("fair.lunchtickets")
def lunchticket_remove(request, year, token):
    fair = get_object_or_404(Fair, year=year)
    lunch_ticket = get_object_or_404(LunchTicket, fair=fair, token=token)

    lunch_ticket.delete()

    return redirect("fair:lunchtickets", fair.year)


@permission_required("fair.lunchtickets")
def lunchticket_send(request, year, token):
    fair = get_object_or_404(Fair, year=year)
    lunch_ticket = get_object_or_404(LunchTicket, fair=fair, token=token)

    eat_by = str(lunch_ticket.time) if lunch_ticket.time else str(lunch_ticket.day)
    email_address = (
        lunch_ticket.user.email if lunch_ticket.user else lunch_ticket.email_address
    )

    send_mail(
        "Lunch ticket " + eat_by,
        "Open the link below to redeem your lunch ticket at "
        + lunch_ticket.fair.name
        + ".\n\nDate: "
        + eat_by
        + "\n"
        + request.build_absolute_uri(
            reverse("lunchticket_display", args=[lunch_ticket.token])
        ),
        "noreply@armada.nu",
        [email_address],
        fail_silently=True,
    )

    LunchTicketSend(
        lunch_ticket=lunch_ticket, user=request.user, email_address=email_address
    ).save()

    lunch_ticket.sent = True
    lunch_ticket.save()

    return redirect("fair:lunchticket", fair.year, lunch_ticket.token)


@permission_required("fair.lunchtickets")
def lunchticket_create(request, year):
    fair = get_object_or_404(Fair, year=year)

    form = LunchTicketForm(request.POST or None, initial={"fair": fair})

    users = []

    for organization_group in OrganizationGroup.objects.filter(fair=fair):
        this_users_flat = [
            application.user
            for application in RecruitmentApplication.objects.select_related("user")
            .filter(
                delegated_role__organization_group=organization_group,
                status="accepted",
                recruitment_period__fair=fair,
            )
            .order_by("user__first_name", "user__last_name")
        ]
        users.append(
            [
                organization_group.name,
                [(user.pk, user.get_full_name()) for user in this_users_flat],
            ]
        )

    form.fields["user"].choices = [("", "---------")] + users

    if request.POST and form.is_valid():
        form.instance.fair = fair
        lunch_ticket = form.save()
        return redirect("fair:lunchticket", fair.year, lunch_ticket.token)

    return render(request, "fair/lunchticket_create.html", {"fair": fair, "form": form})


@permission_required("fair.lunchtickets")
def lunchtickets_check_in(request, year):
    fair = get_object_or_404(Fair, year=year)

    react_props = {}

    return render(
        request,
        "fair/lunch_ticket_check_in.html",
        {"react_props": json.dumps(react_props)},
    )


def lunchticket_display(request, token):
    lunch_ticket = get_object_or_404(LunchTicket, fair__current=True, token=token)

    return render(
        request, "fair/lunchticket_display.html", {"lunch_ticket": lunch_ticket}
    )


def tickets(request, year):
    fair = get_object_or_404(Fair, year=year)
    banquet = Banquet.objects.filter(fair=fair).first()

    lunch_tickets = LunchTicket.objects.filter(fair=fair, user=request.user)
    banquet_participant = Participant.objects.filter(
        user=request.user, banquet=banquet
    ).first()

    react_props = {
        "lunch_tickets": [
            serializers.lunch_ticket(lunch_ticket=lunch_ticket)
            for lunch_ticket in lunch_tickets
        ],
        "banquet_participant": (
            serializers.banquet_participant(banquet_participant)
            if banquet_participant
            else None
        ),
    }

    return render(
        request,
        "fair/tickets.html",
        {"fair": fair, "react_props": json.dumps(react_props)},
    )
