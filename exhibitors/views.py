import datetime
import json

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from accounting.models import Order
from banquet.models import Banquet, Participant
from companies.models import (
    Company,
    CompanyContact,
    CompanyCustomerComment,
    CompanyCustomerResponsible,
)
from exhibitors import serializers
from fair.models import Fair, FairDay, LunchTicket
from recruitment.models import RecruitmentApplication
from register.models import SignupLog
from .forms import (
    ApplicationStatusForm,
    ExhibitorViewForm,
    ExhibitorCreateForm,
    ExhibitorCreateBypassedForm,
    TransportForm,
    DetailsForm,
    ContactPersonForm,
    CheckInForm,
    CommentForm,
    ExhibitorSearchForm,
    BoothForm,
    ExhibitorInBoothForm,
    CoordinatesForm,
    FairLocationForm,
)
from .models import Exhibitor, ExhibitorView, Booth, ExhibitorInBooth, Location, User

from dal import autocomplete
from django.utils.html import format_html
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat


def possible_contact_persons(fair):
    contact_persons = []

    for application in RecruitmentApplication.objects.filter(
        recruitment_period__fair=fair,
        status="accepted",
        delegated_role__allow_exhibitor_contact_person=True,
    ).order_by("recruitment_period", "user__first_name", "user__last_name"):
        user = (application.user.pk, application.user)
        added = False

        for contact_person in contact_persons:
            if contact_person[0] == application.delegated_role:
                contact_person[1].append(user)
                added = True
                break

        if not added:
            contact_persons.append((application.delegated_role, [user]))

    return contact_persons


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = (
            User.objects.order_by("username")
            .annotate(full_name=Concat("first_name", V(" "), "last_name"))
            .all()
        )

        if self.q:
            qs = qs.filter(
                Q(email__istartswith=self.q)
                | Q(username__istartswith=self.q)
                | Q(full_name__icontains=self.q)
            )

        return qs

    def get_result_label(self, result):
        return format_html("{}", result.email)


@permission_required("exhibitors.base")
def exhibitors(request, year, template_name="exhibitors/exhibitors.html"):
    fair = get_object_or_404(Fair, year=year)
    view = ExhibitorView.objects.filter(user=request.user).first()

    if not view:
        view = ExhibitorView(user=request.user).create()

    choices = [] if len(view.choices) == 0 else view.choices.split(" ")

    if "count_lunch_tickets" in choices:
        lunch_tickets_orders = Order.objects.filter(product=fair.product_lunch_ticket)
        lunch_tickets_created = (
            LunchTicket.objects.select_related("company")
            .filter(fair=fair)
            .exclude(company=None)
        )

    if "count_banquet_tickets" in choices:
        products = [
            banquet.product
            for banquet in Banquet.objects.select_related("product")
            .filter(fair=fair)
            .exclude(product=None)
        ]
        banquet_tickets_orders = Order.objects.filter(product__in=products)
        banquet_tickets_created = Participant.objects.filter(
            banquet__in=Banquet.objects.filter(fair=fair).exclude(product=None)
        ).exclude(company=None)

    if "booths" in choices:
        eibs = [
            eib
            for eib in ExhibitorInBooth.objects.select_related("booth__location")
            .select_related("booth__location__parent")
            .filter(exhibitor__fair=fair)
        ]

    exhibitors = []

    for exhibitor in (
        Exhibitor.objects.prefetch_related("contact_persons")
        .filter(fair=fair)
        .order_by("company__name")
    ):
        exhibitors.append(
            {
                "id": exhibitor.pk,
                "name": exhibitor.company.name,
                "exhibitor": exhibitor,
                "fields": [],
            }
        )

    form = ExhibitorSearchForm(request.POST or None)

    form.fields["contact_persons"].choices = possible_contact_persons(fair)

    if request.POST and form.is_valid():
        exhibitors_filtered = []

        for exhibitor in exhibitors:
            for contact_person in form.cleaned_data["contact_persons"]:
                if contact_person in exhibitor["exhibitor"].contact_persons.all():
                    exhibitors_filtered.append(exhibitor)
                    break

        exhibitors = exhibitors_filtered

    if not request.user.has_perm("exhibitors.view_all"):
        exhibitors = [
            exhibitor
            for exhibitor in exhibitors
            if request.user in exhibitor["exhibitor"].contact_persons.all()
        ]

    for exhibitor in exhibitors:
        e = exhibitor["exhibitor"]
        for choice in choices:
            value = None
            if choice == "contact_persons":
                value = e.contact_persons.all()
            if choice == "transport_to":
                value = e.transport_to
            if choice == "transport_from":
                value = e.transport_from
            if choice == "transport_comment":
                value = e.transport_comment
            if choice == "placement_wish":
                value = e.get_placement_wish_display
            if choice == "placement_comment":
                value = e.placement_comment
            if choice == "electricity_total_power":
                value = e.electricity_total_power
            if choice == "electricity_socket_count":
                value = e.electricity_socket_count
            if choice == "electricity_equipment":
                value = e.electricity_equipment
            if choice == "booth_height":
                value = e.booth_height
            if choice == "check_in_timestamp":
                value = e.check_in_timestamp
            if choice == "check_in_comment":
                value = e.check_in_comment
            if choice == "fair_location":
                value = e.fair_location
            if choice == "fair_location_special":
                value = e.fair_location_special

            if choice == "count_lunch_tickets":
                ordered = 0
                created = 0

                for lunch_tickets_order in lunch_tickets_orders:
                    if lunch_tickets_order.purchasing_company == e.company:
                        ordered += lunch_tickets_order.quantity

                for lunch_tickets_create in lunch_tickets_created:
                    if lunch_tickets_create.company == e.company:
                        created += 1

                value = {"ordered": ordered, "created": created}

            if choice == "count_banquet_tickets":
                ordered = 0
                created = 0

                for banquet_tickets_order in banquet_tickets_orders:
                    if banquet_tickets_order.purchasing_company == e.company:
                        ordered += banquet_tickets_order.quantity

                for banquet_tickets_create in banquet_tickets_created:
                    if banquet_tickets_create.company == e.company:
                        created += 1

                value = {"ordered": ordered, "created": created}

            if choice == "booths":
                value = [eib.booth for eib in eibs if eib.exhibitor == e]

            exhibitor["fields"].append({"field": choice, "value": value})

    return render(
        request,
        template_name,
        {"fair": fair, "exhibitors": exhibitors, "fields": choices, "form": form},
    )


@permission_required("exhibitors.base")
def edit_view(request, year, template_name="exhibitors/edit_view.html"):
    view = ExhibitorView.objects.filter(user=request.user).first()
    form = ExhibitorViewForm(request.POST or None, instance=view, user=request.user)

    if form.is_valid():
        form.save()
        return redirect("exhibitors", year)

    return render(
        request,
        template_name,
        {"form": form, "fair": get_object_or_404(Fair, year=year)},
    )


@permission_required("exhibitors.base")
def export(request, year):
    fair = get_object_or_404(Fair, year=year)

    return render(
        request,
        "exhibitors/export.html",
        {"exhibitors": Exhibitor.objects.filter(fair=fair)},
    )


@permission_required("exhibitors.base")
def create(request, year):
    fair = get_object_or_404(Fair, year=year, current=True)
    exhibitors = Exhibitor.objects.filter(fair=fair)
    companies_already_added = []

    for exhibitor in exhibitors:
        companies_already_added.append(exhibitor.company)

    signatures = SignupLog.objects.filter(contract__fair=fair)
    eligible_companies = []

    for signature in signatures:
        if (
            signature.company not in eligible_companies
            and signature.company not in companies_already_added
        ):
            eligible_companies.append(signature.company)

    if len(eligible_companies) != 0:
        form = ExhibitorCreateForm(
            request.POST if request.POST and request.POST.get("add_eligible") else None
        )

        eligible_companies.sort(key=lambda x: x.name)
        form.fields["companies"].choices = [
            (company.pk, company.name) for company in eligible_companies
        ]
    else:
        form = None

    bypass_allowed = False
    if datetime.datetime.now() > fair.complete_registration_start_date:
        bypass_allowed = True

    all_companies = Company.objects.all()
    non_IR_companies = []

    for company in all_companies:
        if (company not in companies_already_added) and (
            company not in eligible_companies
        ):
            non_IR_companies.append(company)

    form_bypass = ExhibitorCreateBypassedForm(
        request.POST if request.POST and request.POST.get("add_bypassed") else None
    )

    non_IR_companies.sort(key=lambda x: x.name)
    form_bypass.fields["company"].choices = [
        (company.pk, company.name) for company in non_IR_companies
    ]

    if not bypass_allowed:
        form_bypass.fields["company"].disabled = True

    if request.POST:
        if request.POST.get("add_eligible") and form.is_valid():
            for company in form.cleaned_data["companies"]:
                if company in eligible_companies:
                    exhibitor = Exhibitor.objects.create(fair=fair, company=company)
                    exhibitor.save()

        elif (
            request.POST.get("add_bypassed")
            and form_bypass.is_valid()
            and bypass_allowed
        ):
            company = form_bypass.cleaned_data["company"]
            if company in non_IR_companies:
                exhibitor = Exhibitor.objects.create(fair=fair, company=company)
                exhibitor.save()

        return redirect("exhibitors", year)

    return render(
        request,
        "exhibitors/create.html",
        {
            "fair": fair,
            "form": form,
            "form_bypass": form_bypass,
            "bypass_allowed": bypass_allowed,
        },
    )


@permission_required("exhibitors.base")
def exhibitor(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)

    if (
        not request.user.has_perm("exhibitors.view_all")
        and request.user not in exhibitor.contact_persons.all()
    ):
        return HttpResponseForbidden()

    orders = []

    for order in Order.objects.filter(
        purchasing_company=exhibitor.company, product__revenue__fair=fair
    ):
        orders.append(
            {
                "name": order.name if order.name is not None else order.product.name,
                "comment": order.comment,
                "unit_price": order.unit_price
                if order.unit_price is not None
                else order.product.unit_price,
                "quantity": order.quantity,
            }
        )

    form_comment = CommentForm(request.POST or None)

    if request.POST and form_comment.is_valid():
        comment = form_comment.save(commit=False)
        comment.company = exhibitor.company
        comment.user = request.user
        comment.show_in_exhibitors = True
        comment.save()
        form_comment.save()

        form_comment = CommentForm()

    contact_persons = []

    for contact_person in exhibitor.contact_persons.all():
        application = RecruitmentApplication.objects.filter(
            recruitment_period__fair=fair, user=contact_person, status="accepted"
        ).first()

        contact_persons.append(
            {
                "user": contact_person,
                "role": application.delegated_role if application is not None else None,
            }
        )

    for responsible in CompanyCustomerResponsible.objects.select_related(
        "group"
    ).filter(company=exhibitor.company, group__fair=fair):
        for user in responsible.users.all():
            application = RecruitmentApplication.objects.filter(
                recruitment_period__fair=fair, user=user, status="accepted"
            ).first()

            already_found = False

            for contact_person in contact_persons:
                if contact_person["user"] == user:
                    already_found = True
                    break

            if not already_found:
                contact_persons.append(
                    {
                        "user": user,
                        "role": application.delegated_role
                        if application is not None
                        else None,
                    }
                )

    lunch_tickets_count_ordered = 0

    for order in Order.objects.filter(
        purchasing_company=exhibitor.company,
        product=exhibitor.fair.product_lunch_ticket,
    ):
        lunch_tickets_count_ordered += order.quantity

    lunch_tickets_days = []
    lunch_tickets_count_created = 0

    for day in FairDay.objects.filter(fair=fair):
        lunch_tickets = LunchTicket.objects.filter(company=exhibitor.company, day=day)
        lunch_tickets_count_created += len(lunch_tickets)

        lunch_tickets_days.append({"date": day.date, "lunch_tickets": lunch_tickets})

    banquets = []
    banquet_tickets_count_ordered = 0
    banquet_tickets_count_created = 0

    for banquet in Banquet.objects.filter(fair=fair):
        if banquet.product is not None:
            for order in Order.objects.filter(
                purchasing_company=exhibitor.company, product=banquet.product
            ):
                banquet_tickets_count_ordered += order.quantity

        banquet_tickets = Participant.objects.filter(
            banquet=banquet, company=exhibitor.company
        )
        banquet_tickets_count_created += len(banquet_tickets)

        banquets.append({"banquet": banquet, "banquet_tickets": banquet_tickets})

    return render(
        request,
        "exhibitors/exhibitor.html",
        {
            "fair": fair,
            "exhibitor": exhibitor,
            "contacts": CompanyContact.objects.filter(
                company=exhibitor.company, active=True
            ),
            "orders": orders,
            "comments": CompanyCustomerComment.objects.filter(
                company=exhibitor.company,
                show_in_exhibitors=True,
                timestamp__year=fair.year,
            ),
            "form_comment": form_comment,
            "contact_persons": contact_persons,
            "lunch_tickets_count_ordered": lunch_tickets_count_ordered,
            "lunch_tickets_count_created": lunch_tickets_count_created,
            "lunch_tickets_days": lunch_tickets_days,
            "banquet_tickets_count_ordered": banquet_tickets_count_ordered,
            "banquet_tickets_count_created": banquet_tickets_count_created,
            "banquets": banquets,
            "deadline_complete_registration": exhibitor.deadline_complete_registration
            or fair.complete_registration_close_date,
            "booths": [
                eib.booth
                for eib in ExhibitorInBooth.objects.select_related("booth").filter(
                    exhibitor=exhibitor
                )
            ],
            "fair_location": exhibitor.fair_location,
            "fair_location_special": exhibitor.fair_location_special,
        },
    )


@permission_required("exhibitors.modify_transport")
def exhibitor_transport(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)

    form = TransportForm(request.POST or None, instance=exhibitor)

    if request.POST and form.is_valid():
        form.save()
        return redirect("exhibitor", fair.year, exhibitor.pk)

    return render(
        request,
        "exhibitors/exhibitor_transport.html",
        {"fair": fair, "exhibitor": exhibitor, "form": form},
    )


@permission_required("exhibitors.modify_details")
def exhibitor_details(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)

    form = DetailsForm(request.POST or None, instance=exhibitor)

    if request.POST and form.is_valid():
        form.save()
        return redirect("exhibitor", fair.year, exhibitor.pk)

    return render(
        request,
        "exhibitors/exhibitor_details.html",
        {"fair": fair, "exhibitor": exhibitor, "form": form},
    )


@permission_required("exhibitors.modify_coordinates")
def exhibitor_coordinates(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)

    form = CoordinatesForm(request.POST or None, instance=exhibitor)

    if request.POST and form.is_valid():
        form.save()
        return redirect("exhibitor", fair.year, exhibitor.pk)

    return render(
        request,
        "exhibitors/exhibitor_coordinates.html",
        {"fair": fair, "exhibitor": exhibitor, "form": form},
    )


@permission_required("exhibitors.modify_fair_location")
def exhibitor_fair_location(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)

    form = FairLocationForm(request.POST or None, instance=exhibitor)

    if request.POST and form.is_valid():
        form.save()
        return redirect("exhibitor", fair.year, exhibitor.pk)

    return render(
        request,
        "exhibitors/exhibitor_fair_location.html",
        {"fair": fair, "exhibitor": exhibitor, "form": form},
    )


@permission_required("exhibitors.modify_application_status")
def exhibitor_application_status(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)

    form = ApplicationStatusForm(request.POST or None, instance=exhibitor)

    if request.POST and form.is_valid():
        form.save()
        return redirect("exhibitor", fair.year, exhibitor.pk)

    return render(
        request,
        "exhibitors/exhibitor_application_status.html",
        {"fair": fair, "exhibitor": exhibitor, "form": form},
    )


@permission_required("exhibitors.modify_contact_persons")
def exhibitor_contact_persons(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)

    form = ContactPersonForm(request.POST or None, instance=exhibitor)

    form.fields["contact_persons"].choices = possible_contact_persons(fair)

    if request.POST and form.is_valid():
        form.save()
        return redirect("exhibitor", fair.year, exhibitor.pk)

    return render(
        request,
        "exhibitors/exhibitor_contact_persons.html",
        {"fair": fair, "exhibitor": exhibitor, "form": form},
    )


@permission_required("exhibitors.modify_check_in")
def exhibitor_check_in(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)

    form = CheckInForm(
        request.POST or None, initial={"comment": exhibitor.check_in_comment}
    )

    if request.POST and form.is_valid():
        exhibitor.check_in_comment = form.cleaned_data["comment"]

        if exhibitor.check_in_timestamp is None:
            exhibitor.check_in_timestamp = datetime.datetime.now()
            exhibitor.check_in_user = request.user

        exhibitor.save()

        return redirect("exhibitor", fair.year, exhibitor.pk)

    return render(
        request,
        "exhibitors/exhibitor_check_in.html",
        {"fair": fair, "exhibitor": exhibitor, "form": form},
    )


@permission_required("exhibitors.modify_check_in")
def exhibitor_check_in_revert(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)

    exhibitor.check_in_timestamp = None
    exhibitor.check_in_user = None
    exhibitor.check_in_comment = None
    exhibitor.save()

    return redirect("exhibitor", fair.year, exhibitor.pk)


@permission_required("exhibitors.base")
def exhibitor_comment_edit(request, year, pk, comment_pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)
    comment = get_object_or_404(
        CompanyCustomerComment,
        company=exhibitor.company,
        pk=comment_pk,
        user=request.user,
    )

    form = CommentForm(request.POST or None, instance=comment)

    if request.POST and form.is_valid():
        form.save()
        return redirect("exhibitor", fair.year, exhibitor.pk)

    return render(
        request,
        "exhibitors/exhibitor_comment_edit.html",
        {"fair": fair, "exhibitor": exhibitor, "form": form},
    )


@permission_required("exhibitors.base")
def exhibitor_comment_remove(request, year, pk, comment_pk):
    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)
    comment = get_object_or_404(
        CompanyCustomerComment,
        company=exhibitor.company,
        pk=comment_pk,
        user=request.user,
    )

    comment.delete()

    return redirect("exhibitor", fair.year, exhibitor.pk)


@permission_required("exhibitors.modify_booths")
def booths(request, year):
    fair = get_object_or_404(Fair, year=year)

    eibs = {}

    for eib in (
        ExhibitorInBooth.objects.select_related("exhibitor")
        .select_related("booth")
        .filter(exhibitor__fair=fair)
    ):
        if eib.booth in eibs:
            eibs[eib.booth].append(eib.exhibitor)
        else:
            eibs[eib.booth] = [eib.exhibitor]

    return render(
        request,
        "exhibitors/booths.html",
        {
            "fair": fair,
            "booths": [
                {
                    "pk": booth.pk,
                    "location": booth.location,
                    "name": booth.name,
                    "exhibitors": eibs[booth] if booth in eibs else [],
                }
                for booth in Booth.objects.filter(location__fair=fair)
            ],
        },
    )


@permission_required("exhibitors.modify_booths")
def booth(request, year, booth_pk):
    fair = get_object_or_404(Fair, year=year)
    booth = get_object_or_404(Booth, location__fair=fair, pk=booth_pk)

    form = BoothForm(request.POST or None, instance=booth)

    form.fields["location"].queryset = Location.objects.exclude(background="")

    if request.POST and form.is_valid():
        form.save()

    return render(
        request,
        "exhibitors/booth.html",
        {
            "fair": fair,
            "booth": booth,
            "form": form,
            "eibs": ExhibitorInBooth.objects.filter(booth=booth),
        },
    )


def people_count(request, year, location_pk):
    location = get_object_or_404(
        Location, fair__year=year, pk=location_pk, people_count_enabled=True
    )

    return render(
        request,
        "exhibitors/people_count.html",
        {"fair": location.fair, "location": location},
    )


@permission_required("exhibitors.modify_booths")
def exhibitor_in_booth_form(request, year, booth_pk, exhibitor_pk=None):
    fair = get_object_or_404(Fair, year=year)
    booth = get_object_or_404(Booth, pk=booth_pk, location__fair=fair)
    exhibitor_in_booth = (
        get_object_or_404(
            ExhibitorInBooth,
            booth=booth,
            exhibitor__pk=exhibitor_pk,
            exhibitor__fair=fair,
        )
        if exhibitor_pk
        else None
    )

    form = ExhibitorInBoothForm(request.POST or None, instance=exhibitor_in_booth)

    form.instance.booth = booth

    form.fields["exhibitor"].queryset = Exhibitor.objects.filter(fair=fair)

    if request.POST and form.is_valid():
        form.save()
        return redirect("booth", fair.year, booth.pk)

    return render(
        request,
        "exhibitors/booth_exhibitor_form.html",
        {"fair": fair, "booth": booth, "form": form, "eib": exhibitor_in_booth},
    )


@permission_required("exhibitors.modify_booths")
def exhibitor_in_booth_remove(request, year, booth_pk, exhibitor_pk):
    fair = get_object_or_404(Fair, year=year)
    eib = get_object_or_404(
        ExhibitorInBooth,
        exhibitor__pk=exhibitor_pk,
        exhibitor__fair=fair,
        booth__pk=booth_pk,
    )

    eib.delete()

    return redirect("booth", fair.year, booth_pk)


@permission_required("exhibitors.base")
def booth_placement(request, year):
    fair = get_object_or_404(Fair, year=year)

    locations_with_maps = Location.objects.exclude(background__exact="").all()

    react_props = {
        "locations": [
            serializers.location(location) for location in locations_with_maps
        ]
    }

    return render(
        request,
        "exhibitors/booth_placement.html",
        {"fair": fair, "react_props": json.dumps(react_props)},
    )
