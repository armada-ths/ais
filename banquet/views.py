import csv
import datetime
import json

import stripe
from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.core.mail import send_mail
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    TemplateView,
    RedirectView,
    UpdateView,
)
from django.core.exceptions import ObjectDoesNotExist


from accounting.models import Order
from banquet.functions import send_confirmation_email, send_invitation_mail
from fair.models import Fair
from people.models import Profile
from recruitment.models import OrganizationGroup, RecruitmentApplication
from util.email import send_mail as send_mail_util
from .forms import (
    InternalParticipantForm,
    ExternalParticipantForm,
    SendInvitationForm,
    InvitationForm,
    ImportInvitationsForm,
    InvitationSearchForm,
    ParticipantForm,
    ParticipantAdminForm,
    AfterPartyInvitationForm,
    AfterPartyTicketForm,
    ParticipantTableMatchingForm,
)
from .models import (
    Banquet,
    Participant,
    InvitationGroup,
    Invitation,
    AfterPartyTicket,
    AfterPartyInvitation,
    Table,
    Seat,
    TableMatching,
)


# External Invite
class ExternalInviteRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        """
        Check if object exists by token
        if it does send to updateview
        """
        invitation = get_object_or_404(Invitation, token=self.kwargs["token"])
        if invitation.participant:
            return reverse_lazy(
                "external_invite_update", kwargs=self.kwargs, current_app="banquet"
            )
        else:
            return reverse_lazy(
                "external_invite_create", kwargs=self.kwargs, current_app="banquet"
            )


class ExternalInviteUpdateView(UpdateView):
    """
    UpdateView for external
    """

    model = Participant
    form_class = ExternalParticipantForm
    template_name = "banquet/invite.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Get invitation object
        """
        self.invitation = get_object_or_404(Invitation, token=self.kwargs["token"])
        self.participant = self.invitation.participant
        self.year = self.invitation.banquet.fair.year
        return super(ExternalInviteUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        Set partipant as what we are updating
        """
        return self.participant

    def get_success_url(self):
        """
        We have some kwargs e.g. year that we need to send
        """
        return reverse_lazy(
            "external_invite_thankyou",
            kwargs={"year": self.kwargs["year"]},
            current_app="banquet",
        )

    def get_context_data(self, **kwargs):
        """
        Adding year
        """
        context = super(ExternalInviteUpdateView, self).get_context_data(**kwargs)
        context["year"] = self.year
        return context


class ExternalInviteCreateView(CreateView):
    """
    Invite view for students and invitees (excl. companies)
    """

    form_class = ExternalParticipantForm
    template_name = "banquet/invite.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if valid token
        """
        token = self.kwargs["token"]

        if not Invitation.objects.filter(token=token).exists():
            return HttpResponseForbidden()
        self.invitation = get_object_or_404(Invitation, token=token)

        if self.invitation.participant:
            return redirect(
                reverse_lazy(
                    "external_invite_update", kwargs=self.kwargs, current_app="banquet"
                )
            )
        else:
            self.year = self.invitation.banquet.fair.year
            return super(ExternalInviteCreateView, self).dispatch(
                request, *args, **kwargs
            )

    def get_success_url(self):
        """
        We have some kwargs e.g. year that we need to send
        """
        return reverse_lazy(
            "external_invite_thankyou", kwargs=self.kwargs, current_app="banquet"
        )

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(ExternalInviteCreateView, self).get_initial()
        # kinda ugly, prob better to modify model
        initial["name"] = self.invitation.name
        initial["email_address"] = self.invitation.email_address

        return initial

    def get_context_data(self, **kwargs):
        """
        Adding year
        """
        context = super(ExternalInviteCreateView, self).get_context_data(**kwargs)
        context["year"] = self.year
        return context

    def form_valid(self, form):
        form.instance.banquet = self.invitation.banquet
        form.instance.email_address = self.invitation.email_address
        self.object = form.save()
        self.invitation.participant = self.object
        self.invitation.save()
        return super(ExternalInviteCreateView, self).form_valid(form)


class GeneralMixin(object):
    """
    Shared functions of Banquet pages
    We will always need to add use some parameters e.g. year banquet
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Adding year, fair as parameters
        """
        self.user = self.request.user
        self.year = self.kwargs["year"]
        self.fair = get_object_or_404(Fair, year=self.year)
        # TODO: Allow for multiple banquets in a year
        self.banquet = Banquet.objects.get(fair=self.fair)

        return super(GeneralMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adding fair,year to our context for consistency with other templates
        """
        context = super(GeneralMixin, self).get_context_data(**kwargs)
        context["year"] = self.year
        context["fair"] = self.fair
        return context


class InternalInviteRedirectView(GeneralMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        invitation = get_object_or_404(
            Invitation, token=self.kwargs["token"], user=self.request.user
        )
        # actual redirect
        if invitation.participant:
            return reverse_lazy(
                "internal_invite_update", kwargs=self.kwargs, current_app="banquet"
            )
        else:
            return reverse_lazy(
                "internal_invite_create", kwargs=self.kwargs, current_app="banquet"
            )


class InternalInviteUpdateView(GeneralMixin, UpdateView):
    """
    Invite view for already registered students
    """

    model = Participant
    form_class = InternalParticipantForm
    template_name = "banquet/internal_invite.html"

    def get_object(self):
        """
        Which object are we updating
        """
        return get_object_or_404(
            Invitation, token=self.kwargs["token"], user=self.request.user
        )

    def get_success_url(self):
        """
        We have some kwargs e.g. year that we need to send
        """
        return reverse_lazy(
            "invite_list", kwargs={"year": self.kwargs["year"]}, current_app="banquet"
        )


class InternalInviteCreateView(GeneralMixin, CreateView):
    """
    Invite view for already registered students
    """

    form_class = InternalParticipantForm
    template_name = "banquet/internal_invite.html"

    def dispatch(self, request, *args, **kwargs):
        """
        For security
        Redirects to updateview if object exists
        """
        self.user = self.request.user
        self.year = self.kwargs["year"]
        self.token = self.kwargs["token"]
        self.invitation = get_object_or_404(
            Invitation, token=self.token, user=self.request.user
        )
        if self.invitation.participant:
            return redirect(
                reverse_lazy(
                    "internal_invite_update", kwargs=self.kwargs, current_app="banquet"
                )
            )
        self.banquet = self.invitation.banquet
        self.user_profile = Profile.objects.get(user=self.user)
        return super(InternalInviteCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(InternalInviteCreateView, self).get_initial()
        # kinda ugly, prob better to modify model
        initial["name"] = self.user.get_full_name()
        initial["email_address"] = self.user.email
        initial["phone_number"] = self.user_profile.phone_number

        return initial

    def get_success_url(self):
        """
        We have some kwargs e.g. year that we need to send
        """
        return reverse_lazy(
            "invite_list", kwargs={"year": self.kwargs["year"]}, current_app="banquet"
        )

    def form_valid(self, form):
        """
        Modified so form doesn't need to have user, banquet
        Also creates an invitation
        """
        form.instance.banquet = self.invitation.banquet
        form.instance.user = self.user
        self.object = form.save()
        self.invitation.participant = self.object
        self.invitation.save()
        return super(InternalInviteCreateView, self).form_valid(form)


class SendInviteCreateView(GeneralMixin, CreateView):
    """
    Banquet group can set who to invite
    """

    form_class = SendInvitationForm
    template_name = "banquet/send_invite.html"

    def get_success_url(self):
        return reverse_lazy("invite_list", kwargs=self.kwargs, current_app="banquet")

    def form_valid(self, form):
        if form.instance.user:
            form.instance.name = form.instance.user.get_full_name()
            form.instance.email_address = form.instance.user.email

        form.instance.banquet = self.banquet
        return super(SendInviteCreateView, self).form_valid(form)


def export_invitations(request, year):
    """
    Exports invitations of banquet
    so we can send out mail(not through ais)
    """
    # here's why I prefer class based views
    # I already did this before >:(
    fair = get_object_or_404(Fair, year=year)
    banquet = Banquet.objects.get(fair=fair)
    invitations = Invitation.objects.filter(banquet=banquet)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="banquet_invitations.csv"'

    writer = csv.writer(response, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerow(["name", "email_address", "invite_link"])
    for invitation in invitations:
        token = invitation.token
        # if external
        if invitation.user is None:
            link = request.build_absolute_uri(
                reverse(
                    "external_invite_redirect",
                    kwargs={"token": token},
                )
            )
        else:
            link = request.build_absolute_uri(
                reverse(
                    "internal_invite_redirect", kwargs={"year": year, "token": token}
                )
            )
        writer.writerow([invitation.name, invitation.email_address, link])
        token = None
    return response


@login_required
def dashboard(request, year):
    fair = get_object_or_404(Fair, year=year)
    current_banquet = Banquet.objects.filter(
        fair=fair
    ).first()  # This might be dangerous, assumes there is only one banquet per fair
    invite_form = AfterPartyInvitationForm()

    # Handle after party invitation request
    if request.method == "POST":
        invite_form = AfterPartyInvitationForm(request.POST)

        if invite_form.is_valid():
            invite = invite_form.save(commit=False)
            # Set the banquet and inviter manually before saving to the database
            invite.banquet = current_banquet
            invite.inviter = request.user

            try:
                invite.save()
                price = str(current_banquet.afterparty_price_discount)
                location = current_banquet.location
                date = current_banquet.afterparty_date

                try:
                    send_mail_util(
                        request,
                        "banquet/email/after_party_invite.html",
                        context={
                            "name": invite.name,
                            "inviter": invite.inviter.get_full_name(),
                            "date": date,
                            "location": location,
                            "price": price,
                            "year": fair.year,
                        },
                        subject="Your invite to the Armada After Party",
                        to=[invite.email_address],
                    )
                except Exception as e:
                    invite_form.add_error(
                        "email_address",
                        "Failed to send e-mail (contact support@armada.nu for help)",
                    )

            except IntegrityError as e:
                # This will catch the uniqueness constraint between banquet/email
                invite_form.add_error(
                    "email_address",
                    "An invitation to this year's after party has already been sent to this e-mail address!",
                )

    banquets = []

    for banquet in Banquet.objects.filter(fair=fair):
        banquets.append(
            {
                "pk": banquet.pk,
                "name": banquet.name,
                "date": banquet.date,
                "location": banquet.location,
                "count_going": Participant.objects.filter(banquet=banquet).count(),
                "count_not_going": Invitation.objects.filter(
                    banquet=banquet, denied=True
                ).count(),
                "count_pending": Invitation.objects.filter(
                    banquet=banquet, participant=None
                )
                .exclude(denied=True)
                .count(),
            }
        )

    # Any Armada member can invite friends to the after-party
    # during a time period before the current fair
    invitation_period = False
    fair_date = current_banquet.date if current_banquet else None
    now = datetime.date.today()
    if fair_date:
        days_until_fair = (fair_date.date() - now).days
        if (
            0 <= days_until_fair <= 30
        ):  # Invitations are allowed 30 days before the fair (if a banquet has been created...)
            invitation_period = True

    after_party_invites = []
    # All the people this person has invited to the after party
    # We don't really need to do this if invitation_period = False
    for invite in AfterPartyInvitation.objects.filter(
        inviter=request.user, banquet=current_banquet
    ):
        after_party_invites.append({"name": invite.name, "email": invite.email_address})

    # Only people who are currently part of Armada may invite other people
    auth_users = [
        recruitment_application.user
        for recruitment_application in RecruitmentApplication.objects.filter(
            status="accepted", recruitment_period__fair=fair
        )
    ]
    invite_permission = request.user in auth_users

    max_invites = 5  # The number of people someone may invite to the after party

    # Any Armada member can invite friends to the after-party
    # during a time period before the current fair
    invitation_period = False
    fair_date = current_banquet.date if current_banquet else None
    now = datetime.date.today()
    if fair_date:
        days_until_fair = (fair_date.date() - now).days
        if (
            0 <= days_until_fair <= 30
        ):  # Invitations are allowed 30 days before the fair (if there is a fair by then...)
            invitation_period = True

    after_party_invites = []
    # All the people this person has invited to the after party
    # We don't really need to do this if invitation_period = False
    for invite in AfterPartyInvitation.objects.filter(
        inviter=request.user, banquet__fair=fair
    ):
        after_party_invites.append({"name": invite.name, "email": invite.email_address})

    # Only people who are currently part of armada PM, PG or OT may invite other people
    auth_users = [
        recruitment_application.user
        for recruitment_application in RecruitmentApplication.objects.filter(
            status="accepted",
            recruitment_period__fair=fair,
        ).exclude(
            recruitment_period__name__contains="Host",
        )
    ]

    invite_permission = request.user in auth_users

    max_invites = 2

    # For using after party-invitations, change False to invitation_period
    return render(
        request,
        "banquet/dashboard.html",
        {
            "fair": fair,
            "invitiations": Invitation.objects.filter(user=request.user),
            "banquets": banquets,
            "after_party_invites": {
                "invites": after_party_invites,
                "form": invite_form,
                "show": invite_permission and invitation_period,
                "show_form": len(after_party_invites)
                < max_invites,  # Can be used in the template to check whether invitation form should be presented
                "left": max_invites - len(after_party_invites),
            },
        },
    )


@permission_required("banquet.base")
def manage(request, year, banquet_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)

    count_ordered = 0
    for order in Order.objects.filter(product=banquet.product):
        count_ordered += order.quantity

    count_after_party_invited_sold = 0
    used_invitations = AfterPartyInvitation.objects.filter(banquet=banquet, used=True)
    for invitation in used_invitations:
        ticket = AfterPartyTicket.objects.filter(
            banquet=banquet, email_address=invitation.email_address, has_paid=True
        ).count()
        if ticket > 0:
            count_after_party_invited_sold += 1

    return render(
        request,
        "banquet/manage.html",
        {
            "fair": fair,
            "banquet": banquet,
            "count_going": Invitation.objects.filter(banquet=banquet)
            .exclude(participant=None)
            .count(),
            "count_not_going": Invitation.objects.filter(
                banquet=banquet, denied=True
            ).count(),
            "count_invitations": Invitation.objects.filter(banquet=banquet).count(),
            "count_pending": Invitation.objects.filter(
                banquet=banquet, denied=False, participant=None
            ).count(),
            "count_ordered": count_ordered,
            "count_created": Participant.objects.filter(banquet=banquet)
            .exclude(company=None)
            .count(),
            "count_participants": Participant.objects.filter(banquet=banquet).count(),
            "count_after_party": AfterPartyTicket.objects.filter(
                banquet=banquet, has_paid=True
            ).count(),
            "count_after_party_invited_total": AfterPartyInvitation.objects.filter(
                banquet=banquet
            ).count(),
            "count_after_party_invited_sold": count_after_party_invited_sold,
        },
    )


@permission_required("banquet.base")
def manage_map(request, year, banquet_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)
    seats_taken = {}

    for participant in Participant.objects.filter(banquet=banquet).exclude(seat=None):
        seats_taken[participant.seat] = str(participant)

    seats = json.dumps(
        [
            {
                "id": seat.pk,
                "name": seat.name,
                "table": seat.table.name,
                "top": seat.top,
                "left": seat.left,
                "participant": seats_taken[seat] if seat in seats_taken else None,
            }
            for seat in Seat.objects.filter(table__banquet=banquet)
        ]
    )

    return render(
        request,
        "banquet/manage_map.html",
        {"fair": fair, "banquet": banquet, "seats": seats},
    )


@permission_required("banquet.base")
def manage_invitations(request, year, banquet_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)
    did_error_email = request.GET.get("did_error_email", False)

    invitations = []

    for invitation in (
        Invitation.objects.select_related("user")
        .select_related("group")
        .filter(banquet=banquet)
    ):
        invitations.append(
            {
                "pk": invitation.pk,
                "group": invitation.group,
                "user": invitation.user,
                "name": (
                    invitation.user.get_full_name()
                    if invitation.user is not None
                    else invitation.name
                ),
                "reason": invitation.reason,
                "status": invitation.status,
                "price": invitation.price,
                "deadline_smart": invitation.deadline_smart,
                "matching_status": invitation.part_of_matching,
                "has_sent_mail": invitation.has_sent_mail,
            }
        )

    form = InvitationSearchForm(request.POST or None)

    form.fields["groups"].queryset = InvitationGroup.objects.filter(banquet=banquet)

    has_filtering = request.POST and form.is_valid()

    invitations_modified = []

    for invitation in invitations:
        if has_filtering:
            if len(form.cleaned_data["groups"]) > 0:
                found = False

                for group in form.cleaned_data["groups"]:
                    if invitation["group"] == group:
                        found = True
                        break

                if not found:
                    continue

            if len(form.cleaned_data["statuses"]) > 0:
                found = False

                for status in form.cleaned_data["statuses"]:
                    if invitation["status"] == status:
                        found = True
                        break

                if not found:
                    continue

            if form.cleaned_data[
                "matching_statuses"
            ]:  # '' if choice 'Any' given, 'True' if yes, 'False' if no
                if (
                    invitation["matching_status"]
                    and form.cleaned_data["matching_statuses"] != "True"
                ):
                    continue
                if (
                    not invitation["matching_status"]
                    and form.cleaned_data["matching_statuses"] != "False"
                ):
                    continue

        invitations_modified.append(invitation)

    return render(
        request,
        "banquet/manage_invitations.html",
        {
            "fair": fair,
            "banquet": banquet,
            "invitiations": invitations_modified,
            "form": form,
            "did_error_email": did_error_email,
        },
    )


@permission_required("banquet.base")
def manage_invitation(request, year, banquet_pk, invitation_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)
    invitation = get_object_or_404(Invitation, banquet=banquet, pk=invitation_pk)

    return render(
        request,
        "banquet/manage_invitation.html",
        {"fair": fair, "banquet": banquet, "invitation": invitation},
    )


@permission_required("banquet.base")
def manage_handle_email(request, year, banquet_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)

    if request.POST:
        if "unsent" in request.POST:
            invitations = Invitation.objects.filter(
                banquet=banquet, has_sent_mail=False
            )

            did_error_email = False
            sent = 0
            failed = 0

            for invitation in invitations:
                if not send_confirmation_email(
                    request,
                    invitation,
                    invitation.name,
                    invitation.email_address,
                    fair,
                ):
                    did_error_email = True
                    failed += 1
                    continue

                sent += 1

            return redirect(
                reverse(
                    "banquet_handle_email",
                    kwargs={"year": year, "banquet_pk": banquet_pk},
                )
                + "?"
                + (f"&error=Failed to send {failed} emails!" if did_error_email else "")
                + f"&success={sent} emails sent!"
            )

        if "reminderpreview" in request.POST:
            group_id = request.POST["group"]
            if group_id == "":
                return redirect(
                    reverse(
                        "banquet_handle_email",
                        kwargs={"year": year, "banquet_pk": banquet_pk},
                    )
                    + "?error=Must select group"
                )

            group = InvitationGroup.objects.get(pk=group_id)
            did_error_email = False

            if group is None:
                return redirect(
                    reverse(
                        "banquet_handle_email",
                        kwargs={"year": year, "banquet_pk": banquet_pk},
                    )
                    + "?error=Group does not exist"
                )

            invitations = Invitation.objects.filter(
                banquet=banquet,
                has_sent_mail=True,
                group=group,
            )

            invitations = [
                inv for inv in invitations if inv.status not in ["GOING", "NOT_GOING"]
            ]

            return render(
                request,
                "banquet/manage_handle_email.html",
                {
                    "fair": fair,
                    "banquet": banquet,
                    "error": False,
                    "success": False,
                    "remindergroup": group,
                    "invitations": invitations,
                },
            )

        if "reminder" in request.POST:
            group = InvitationGroup.objects.get(pk=request.POST["group"])
            invitations = request.POST.getlist("invitations[]")
            invitations = Invitation.objects.filter(pk__in=invitations)

            did_error_email = False
            sent = 0
            failed = 0

            for invitation in invitations:
                if not send_confirmation_email(
                    request,
                    invitation,
                    invitation.name,
                    invitation.email_address,
                    fair,
                    template="banquet/email/reminder.html",
                    subject="Reminder: THS Armada Banquet Confirmation",
                ):
                    did_error_email = True
                    failed += 1
                    continue

                sent += 1

            return redirect(
                reverse(
                    "banquet_handle_email",
                    kwargs={"year": year, "banquet_pk": banquet_pk},
                )
                + "?"
                + (f"&error=Failed to send {failed} emails!" if did_error_email else "")
                + f'&success={sent} emails sent for group "{group}"!'
            )

    invitations = Invitation.objects.filter(banquet=banquet, has_sent_mail=False)

    return render(
        request,
        "banquet/manage_handle_email.html",
        {
            "fair": fair,
            "banquet": banquet,
            "error": request.GET.get("error", False),
            "success": request.GET.get("success", False),
            "invitations": invitations,
            "groups": InvitationGroup.objects.filter(banquet=banquet),
        },
    )


@permission_required("banquet.base")
def manage_import_invitations(request, year, banquet_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)

    imported = None
    has_errors = False
    has_warnings = False
    all_invited = False

    form = ImportInvitationsForm(request.POST or None, banquet=banquet)
    form.fields["group"].queryset = InvitationGroup.objects.filter(banquet=banquet)

    if request.POST and form.is_valid():
        imported = form.cleaned_data["excel_text"]
        has_errors = any(
            "invalid_price" in row or "invalid_email" in row for row in imported
        )
        has_warnings = any("invalid_name" in row for row in imported)
        all_invited = all("duplicate" in row for row in imported)

        if "invite" in request.POST:
            send_mail = form.cleaned_data["send_email"]
            group = form.cleaned_data["group"]

            if group is None:
                form.add_error(
                    "group",
                    "You must select a group to invite to the banquet.",
                )
            else:
                did_error_email = False

                for invite in imported:
                    # Invite already exists
                    if Invitation.objects.filter(
                        email_address=invite["email"], banquet=banquet
                    ).exists():
                        continue

                    invitation = Invitation(
                        banquet=banquet,
                        name=invite["name"],
                        email_address=invite["email"],
                        price=invite["price"] or 0,
                        group=group,
                    )

                    invitation.save()

                    if send_mail:
                        if not send_confirmation_email(
                            request,
                            invitation,
                            invite["name"],
                            invite["email"],
                            fair,
                        ):
                            did_error_email = True
                            continue

                        invitation.has_sent_mail = True
                        invitation.save()

                return redirect(
                    reverse(
                        "banquet_manage_invitations",
                        kwargs={"year": year, "banquet_pk": banquet.pk},
                    )
                    + ("?did_error_email=1" if did_error_email else "")
                )

    return render(
        request,
        "banquet/manage_imported_invitations.html",
        {
            "fair": fair,
            "banquet": banquet,
            "form": form,
            "imported": imported,
            "has_errors": has_errors,
            "has_warnings": has_warnings,
            "all_invited": all_invited,
        },
    )


@permission_required("banquet.base")
def manage_invitation_form(request, year, banquet_pk, invitation_pk=None):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)

    invitation = (
        get_object_or_404(Invitation, banquet=banquet, pk=invitation_pk)
        if invitation_pk is not None
        else None
    )

    form = InvitationForm(request.POST or None, instance=invitation)

    users = []
    users_flat = []

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
        users_flat += this_users_flat
        users.append(
            [
                organization_group.name,
                [(user.pk, user.get_full_name()) for user in this_users_flat],
            ]
        )

    if (
        invitation is not None
        and invitation.user is not None
        and invitation.user not in users_flat
    ):
        users = [(invitation.user.pk, invitation.user.get_full_name())] + users

    users = [("", "---------")] + users

    form.fields["user"].choices = users

    groups = [
        (
            group.pk,
            group.name
            + " ("
            + (
                "deadline " + str(group.deadline)
                if group.deadline is not None
                else "no deadline"
            )
            + ")",
        )
        for group in InvitationGroup.objects.filter(banquet=banquet)
    ]

    form.fields["group"].choices = groups

    if invitation is not None and invitation.participant is not None:
        form.fields["price"].disabled = True
        form.fields["price"].help_text = (
            "The price cannot be changed as the invitation has already been accepted."
        )

    if request.POST and form.is_valid():
        form.instance.banquet = banquet
        if invitation == None:
            has_sent_mail = False
        else:
            has_sent_mail = invitation.has_sent_mail

        invitation = form.save()

        if (
            invitation.participant is not None
            and invitation.participant.user is None
            and invitation.participant.company is None
        ):
            invitation.participant.name = invitation.name
            invitation.participant.email_address = invitation.email_address

        if invitation.participant == None:
            # Not participant means not responded to invite
            if invitation.user != None:
                # Internal, get info from user
                name = invitation.user.get_full_name()
                email_address = invitation.user.email
            else:
                # External, info contained in form
                name = invitation.name
                email_address = invitation.email_address
        else:
            # Participant, info from participant instance
            name = invitation.participant.name
            email_address = invitation.participant.email_address

        send_mail = form.cleaned_data["send_email"]

        # Automatically send invite email if it hasn't been sent before
        if send_mail and not has_sent_mail:
            send_confirmation_email(request, invitation, name, email_address, fair)
            form.instance.has_sent_mail = True
            form.save()

        return redirect(
            "banquet_manage_invitation", fair.year, banquet.pk, invitation.pk
        )

    return render(
        request,
        "banquet/manage_invitation_form.html",
        {"fair": fair, "banquet": banquet, "invitation": invitation, "form": form},
    )


@permission_required("banquet.base")
def manage_participant(request, year, banquet_pk, participant_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)
    participant = get_object_or_404(Participant, banquet=banquet, pk=participant_pk)

    try:
        invitation = participant.invitation_set.first()
        invitation_status = invitation.status
    except:
        invitation = None
        invitation_status = None

    return render(
        request,
        "banquet/manage_participant.html",
        {
            "fair": fair,
            "banquet": banquet,
            "invitation": invitation,
            "participant": {
                "pk": participant.pk,
                "name": (
                    participant.user.get_full_name()
                    if participant.user
                    else participant.name
                ),
                "email_address": (
                    participant.user.email
                    if participant.user
                    else participant.email_address
                ),
                "phone_number": participant.phone_number,
                "dietary_preference": participant.dietary_preference,
                "dietary_restrictions": participant.dietary_restrictions,
                "other_dietary_restrictions": participant.other_dietary_restrictions,
                "alcohol": participant.get_alcohol_display,
                "giveaway": participant.get_giveaway_display,
                "token": participant.token,
                "seat": participant.seat,
                "invitation_status": invitation_status,
            },
        },
    )


def get_dietary_string(participant):
    other_preferences = list(
        participant.dietary_restrictions.values_list("name", flat=True)
    )

    if participant.other_dietary_restrictions:
        other_preferences += [participant.other_dietary_restrictions]

    addition = "" if not other_preferences else f" ({', '.join(other_preferences)})"

    return f"{participant.dietary_preference}{addition}"


@permission_required("banquet.base")
def manage_participants(request, year, banquet_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)

    participants = [
        {
            "pk": participant.pk,
            "company": participant.company,
            "user": participant.user,
            "name": (
                participant.user.get_full_name()
                if participant.user
                else participant.name
            ),
            "email_address": (
                participant.user.email
                if participant.user
                else participant.email_address
            ),
            "dietary": get_dietary_string(participant),
            "alcohol": participant.alcohol,
            "seat": participant.seat,
            "invitation": participant.invitation_set.first(),
        }
        for participant in Participant.objects.select_related("seat")
        .select_related("seat__table")
        .filter(banquet=banquet)
    ]

    return render(
        request,
        "banquet/manage_participants.html",
        {"fair": fair, "banquet": banquet, "participants": participants},
    )


@permission_required("banquet.base")
def manage_participant_form(request, year, banquet_pk, participant_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)
    participant = get_object_or_404(Participant, banquet=banquet, pk=participant_pk)

    form = ParticipantAdminForm(request.POST or None, instance=participant)

    seats_taken = [
        p.seat for p in Participant.objects.select_related("seat").exclude(seat=None)
    ]

    if participant is not None and participant.seat is not None:
        seats_taken.remove(participant.seat)

    seats = []

    for table in Table.objects.filter(banquet=banquet):
        table_seats = []

        for table_seat in Seat.objects.filter(table=table):
            if table_seat not in seats_taken:
                table_seats.append((table_seat.pk, table_seat.name))

        seats.append([table.name, table_seats])

    form.fields["seat"].choices = [("", "---------")] + seats

    users = []
    all_users = []

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
        all_users += this_users_flat
        users.append(
            [
                organization_group.name,
                [(user.pk, user.get_full_name()) for user in this_users_flat],
            ]
        )

    if (
        participant is not None
        and participant.user is not None
        and participant.user not in all_users
    ):
        users = [(participant.user.pk, participant.user.get_full_name())] + users

    form.fields["user"].choices = [("", "---------")] + users

    if request.POST and form.is_valid():
        participant = form.save()

        invitation = Invitation.objects.filter(participant=participant).first()

        if invitation is not None:
            invitation.user = participant.user
            invitation.name = participant.name
            invitation.email_address = participant.email_address
            invitation.save()

        return redirect("banquet_manage_participants", fair.year, banquet.pk)

    return render(
        request,
        "banquet/manage_participant_form.html",
        {"fair": fair, "banquet": banquet, "form": form, "participant": participant},
    )


@permission_required("banquet.base")
def manage_participant_remove(request, year, banquet_pk, participant_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)
    participant = get_object_or_404(Participant, banquet=banquet, pk=participant_pk)

    participant.delete()

    return redirect("banquet_manage_participants", fair.year, banquet.pk)


def invitation(request, year, token):
    fair = get_object_or_404(Fair, year=year)
    invitation = get_object_or_404(
        Invitation, banquet__fair=fair, token=token, user=request.user
    )

    participant = (
        invitation.participant
        if invitation.participant is not None
        else Participant(banquet=invitation.banquet, user=request.user)
    )
    try:
        existingTableMatching = TableMatching.objects.get(participant=participant)
    except ObjectDoesNotExist:
        existingTableMatching = None

    tableMatching = (
        existingTableMatching if existingTableMatching is not None else TableMatching()
    )
    participant.name = request.user.get_full_name()
    participant.email_address = request.user.email
    tableMatchingForm = ParticipantTableMatchingForm(
        request.POST or None, instance=tableMatching
    )

    form = ParticipantForm(request.POST or None, instance=participant)
    form.fields["phone_number"].required = True

    if invitation.banquet.caption_phone_number is not None:
        form.fields["phone_number"].help_text = invitation.banquet.caption_phone_number
    if invitation.banquet.caption_dietary_restrictions is not None:
        form.fields["dietary_restrictions"].help_text = (
            invitation.banquet.caption_dietary_restrictions
        )

    can_edit = (
        invitation.deadline_smart is None
        or invitation.deadline_smart >= datetime.datetime.now().date()
    )

    if can_edit:
        if request.POST and form.is_valid():
            form.instance.name = None
            form.instance.email_address = None
            invitation.participant = form.save()
            invitation.save()

            tableMatchingForm.instance.participant = invitation.participant

            if invitation.part_of_matching:
                tableMatchingForm.save()

            if (
                invitation.price > 0 and invitation.participant.has_paid == False
            ):  # should pay a price and has not done this already
                stripe.api_key = settings.STRIPE_SECRET
                # Create or retrieve a Stripe payment intent https://stripe.com/docs/payments/payment-intents/web
                if invitation.participant.charge_stripe == None:
                    intent = stripe.PaymentIntent.create(
                        amount=invitation.price * 100,  # Stripe wants the price in öre
                        currency="sek",
                        description="Banquet invitation token " + str(invitation.token),
                        receipt_email=invitation.email_address,
                    )
                    invitation.participant.charge_stripe = intent["id"]
                    invitation.participant.save()
                else:  # retrieve existing payment intent
                    intent = stripe.PaymentIntent.retrieve(
                        invitation.participant.charge_stripe
                    )

                request.session["event"] = "Banquet"
                request.session["intent"] = intent
                request.session["invitation_token"] = token
                request.session["url_path"] = (
                    "/fairs/" + str(fair.year) + "/banquet/invitation/" + token
                )
                request.session.set_expiry(0)  # session expires on browser close
                return redirect("/payments/checkout")

            form = None

    else:
        form = None

    return render(
        request,
        "banquet/invitation_internal.html",
        {
            "fair": fair,
            "invitation": invitation,
            "form": form,
            "charge": invitation.price > 0
            and (
                invitation.participant is None
                or invitation.participant.has_paid == False
            ),
            "stripe_publishable": settings.STRIPE_PUBLISHABLE,
            "stripe_amount": invitation.price * 100,
            "can_edit": can_edit,
            "form_catalogue_details": tableMatchingForm,
            "participant": {"token": participant.token},
        },
    )


@permission_required("banquet.base")
def send_invitation_button(request, year, banquet_pk, invitation_pk):
    """Called when "Send invitation Mail" is pressed on the manage_invitation page."""

    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)
    invitation = get_object_or_404(Invitation, banquet=banquet, pk=invitation_pk)

    if invitation.user is None:
        name = invitation.name
        email = invitation.email_address
        link = request.build_absolute_uri(
            reverse(
                "banquet_external_invitation",
                kwargs={"token": invitation.token},
            )
        )
    else:
        name = invitation.user.get_full_name()
        email = invitation.user.email
        link = request.build_absolute_uri(
            reverse(
                "banquet_invitation",
                kwargs={"year": year, "token": invitation.token},
            )
        )

    if send_invitation_mail(
        request,
        invitation,
        name,
        banquet,
        link,
        email,
        fair,
    ):
        return render(
            request,
            "banquet/invite_sent.html",
            {
                "fair": fair,
            },
        )

    return redirect(
        "banquet_manage_invitations",
        year,
        banquet.pk,
    )


def invitation_no(request, year, token):
    fair = get_object_or_404(Fair, year=year)
    invitation = get_object_or_404(
        Invitation, banquet__fair=fair, token=token, user=request.user
    )

    if (
        invitation.deadline_smart is not None
        and datetime.datetime.now().date() > invitation.deadline_smart
    ):
        return HttpResponseForbidden()

    if invitation.participant is not None:
        if invitation.participant.charge_stripe is not None:
            try:
                del request.session["intent"]
            except KeyError:
                pass
            # Stripe refund: https://stripe.com/docs/payments/cards/refunds
            stripe.api_key = settings.STRIPE_SECRET
            intent = stripe.PaymentIntent.retrieve(invitation.participant.charge_stripe)
            if invitation.participant.has_paid:
                intent["charges"]["data"][0].refund()
            else:
                intent.cancel(cancellation_reason="requested_by_customer")

        invitation.participant.delete()
        invitation.participant = None

    invitation.denied = True
    invitation.save()

    return redirect("banquet_invitation", fair.year, invitation.token)


def invitation_maybe(request, year, token):
    fair = get_object_or_404(Fair, year=year)
    invitation = get_object_or_404(
        Invitation, banquet__fair=fair, token=token, user=request.user
    )

    if (
        invitation.deadline_smart is not None
        and datetime.datetime.now().date() > invitation.deadline_smart
    ):
        return HttpResponseForbidden()

    invitation.denied = False
    invitation.save()

    return redirect("banquet_invitation", fair.year, invitation.token)


def external_invitation(request, token):
    invitation = get_object_or_404(Invitation, token=token, user=None)
    # get participant or create a new one with correct name and email prefilled in participant form
    participant = (
        invitation.participant
        if invitation.participant is not None
        else Participant(banquet=invitation.banquet, user=None)
    )

    participant.name = invitation.name
    participant.email_address = invitation.email_address

    try:
        existingTableMatching = TableMatching.objects.get(participant=participant)
    except ObjectDoesNotExist:
        existingTableMatching = None

    tableMatching = (
        existingTableMatching if existingTableMatching is not None else TableMatching()
    )
    form = ParticipantForm(request.POST or None, instance=participant)
    tableMatchingForm = ParticipantTableMatchingForm(
        request.POST or None, instance=tableMatching
    )
    form.fields["phone_number"].required = True

    if invitation.banquet.caption_phone_number is not None:
        form.fields["phone_number"].help_text = invitation.banquet.caption_phone_number
    if invitation.banquet.caption_dietary_restrictions is not None:
        form.fields["dietary_restrictions"].help_text = (
            invitation.banquet.caption_dietary_restrictions
        )

    can_edit = (
        invitation.deadline_smart is None
        or invitation.deadline_smart >= datetime.datetime.now().date()
    )

    if can_edit:
        if request.POST and form.is_valid():
            form.instance.name = invitation.name
            form.instance.email_address = invitation.email_address
            invitation.participant = form.save()
            invitation.save()

            tableMatchingForm.instance.participant = invitation.participant
            if invitation.part_of_matching:
                tableMatchingForm.save()

            if (
                invitation.price > 0 and invitation.participant.has_paid == False
            ):  # should pay a price and has not done this already
                stripe.api_key = settings.STRIPE_SECRET
                # Create or retrieve a Stripe payment intent https://stripe.com/docs/payments/payment-intents/web
                if invitation.participant.charge_stripe == None:
                    intent = stripe.PaymentIntent.create(
                        amount=invitation.price * 100,  # Stripe wants the price in öre
                        currency="sek",
                        description="Banquet invitation token " + str(invitation.token),
                        receipt_email=invitation.email_address,
                    )
                    invitation.participant.charge_stripe = intent["id"]
                    invitation.participant.save()
                else:  # retrieve existing payment intent
                    intent = stripe.PaymentIntent.retrieve(
                        invitation.participant.charge_stripe
                    )

                request.session["event"] = "Banquet"
                request.session["intent"] = intent
                request.session["invitation_token"] = token
                request.session["url_path"] = "../banquet/" + token
                request.session.set_expiry(0)  # session expires on browser close
                return redirect("../payments/checkout")

            form = None

    else:
        form = None

    return render(
        request,
        "banquet/invitation_external.html",
        {
            "invitation": invitation,
            "form": form,
            "charge": invitation.price > 0
            and (
                invitation.participant is None
                or invitation.participant.has_paid == False
            ),
            "stripe_publishable": settings.STRIPE_PUBLISHABLE,
            "stripe_amount": invitation.price * 100,
            "can_edit": can_edit,
            "form_catalogue_details": tableMatchingForm,
            "participant": {"token": participant.token},
        },
    )


def participant_display(request, token):
    participant = get_object_or_404(Participant, token=token)

    return render(
        request, "banquet/participant_display.html", {"participant": participant}
    )


def external_invitation_no(request, token):
    invitation = get_object_or_404(Invitation, token=token, user=None)

    if (
        invitation.deadline_smart is not None
        and datetime.datetime.now().date() > invitation.deadline_smart
    ):
        return HttpResponseForbidden()

    if invitation.participant is not None:
        if invitation.participant.charge_stripe is not None:
            try:
                del request.session["intent"]
            except KeyError:
                pass
            # Stripe refund: https://stripe.com/docs/payments/cards/refunds
            stripe.api_key = settings.STRIPE_SECRET
            intent = stripe.PaymentIntent.retrieve(invitation.participant.charge_stripe)
            if invitation.participant.has_paid:
                intent["charges"]["data"][0].refund()
            else:
                intent.cancel(cancellation_reason="requested_by_customer")

        invitation.participant.delete()
        invitation.participant = None

    invitation.denied = True
    invitation.save()

    return redirect("banquet_external_invitation", invitation.token)


def external_invitation_maybe(request, token):
    invitation = get_object_or_404(Invitation, token=token, user=None)

    if (
        invitation.deadline_smart is not None
        and datetime.datetime.now().date() > invitation.deadline_smart
    ):
        return HttpResponseForbidden()

    invitation.denied = False
    invitation.save()

    return redirect("banquet_external_invitation", invitation.token)


def external_banquet_afterparty(request, token=None):
    fair = get_object_or_404(Fair, current=True)
    current_banquet = Banquet.objects.filter(fair=fair).first()
    ticket = (
        get_object_or_404(AfterPartyTicket, token=token) if token is not None else None
    )

    date = current_banquet.afterparty_date
    location = current_banquet.location
    amount = current_banquet.afterparty_price
    form = None
    has_paid = False

    day_string = date.date().strftime("%Y-%m-%d")
    purchase_deadline = datetime.datetime.strptime(
        day_string + " 17:00", "%Y-%m-%d %H:%M"
    )

    if ticket is None:
        if timezone.now() <= purchase_deadline:
            form = AfterPartyTicketForm(request.POST or None)

            if request.POST and form.is_valid():
                ticket = form.save(commit=False)
                ticket.banquet = current_banquet
                ticket.save()

                try:
                    discounted_invitation = AfterPartyInvitation.objects.get(
                        email_address=ticket.email_address,
                        banquet=current_banquet,
                        used=False,
                    )
                except:
                    discounted_invitation = None

                if discounted_invitation is not None:
                    amount = current_banquet.afterparty_price_discount
                    discounted_invitation.used = True
                    discounted_invitation.save()

                send_mail(
                    "Your ticket for the After Party",
                    "Hello "
                    + ticket.name
                    + "! Welcome to the After Party at the Grand Banquet of THS Armada."
                    + "\n\nTime and date: "
                    + str(date)
                    + "\nLocation: "
                    + str(location)
                    + "\nThis ticket Costs: "
                    + str(amount)
                    + "\nPayments at the door!"
                    + "\nPlease show this mail at the door!"
                    + "\n\nWelcome!",
                    "noreply@armada.nu",
                    [ticket.email_address],
                    fail_silently=True,
                )
                ticket.email_sent = True
                ticket.save()
                if ticket.email_sent is True:
                    return redirect("https://armada.nu/")

    ###########################################Uncomment this block for payment#####################################################
    #             if amount > 0 and ticket.paid_price is None:
    #                 stripe.api_key = settings.STRIPE_SECRET

    #                 intent = stripe.PaymentIntent.create(
    #                     amount = amount * 100, # Stripe wants the price in öre
    #                     currency = 'sek',
    #                     description ='After party ticket ' + str(ticket.token),
    #                     receipt_email = ticket.email_address,
    #                     )

    #                 ticket.charge_stripe = intent['id']
    #                 ticket.save()

    #                 request.session['event'] = 'AfterParty'
    #                 request.session['url_path'] = 'banquet_external_afterparty_token'
    #                 request.session['intent'] = intent
    #                 request.session['invitation_token'] = str(ticket.token)
    #                 request.session.set_expiry(0)

    #                 return redirect('/payments/checkout')

    # if ticket is not None:
    #     stripe.api_key = settings.STRIPE_SECRET

    #     id = ticket.charge_stripe
    #     amount = (stripe.PaymentIntent.retrieve(id)['amount'])/100
    #     has_paid = ticket.has_paid

    #     if request.POST and ticket.has_paid is False:
    #         if timezone.now() <= purchase_deadline:

    #             request.session['event'] = 'AfterParty'
    #             request.session['url_path'] = 'banquet_external_afterparty_token'
    #             request.session['intent'] = stripe.PaymentIntent.retrieve(id)
    #             request.session['invitation_token'] = str(ticket.token)
    #             request.session.set_expiry(0)

    #             return redirect('/payments/checkout')

    #     if ticket.charge_stripe is not None:
    #         stripe.api_key = settings.STRIPE_SECRET

    #         if stripe.PaymentIntent.retrieve(ticket.charge_stripe)['status'] == 'succeeded' and ticket.email_sent == False:
    #     send_mail(
    #     'Your ticket for the After Party',
    #     'Hello ' + ticket.name + '! Welcome to the After Party at the Grand Banquet of THS Armada. Your ticket is available here:\nhttps://ais.armada.nu/banquet/afterparty/' + str(
    #         ticket.token) + '\n\nTime and date: ' + str(date) + '\nLocation: ' + str(location) + '\n\nWelcome!',
    #     'noreply@armada.nu',
    #     [ticket.email_address],
    #     fail_silently=True,
    # )
    # ticket.email_sent = True
    # ticket.save()
    ###########################################Uncomment this block for payment#####################################################

    return render(
        request,
        "banquet/afterparty.html",
        {
            "fair": fair,
            "form": form,
            "date": date,
            "location": location,
            "stripe_publishable": settings.STRIPE_PUBLISHABLE,
            "amount": amount,
            "ticket": ticket,
            "has_paid": has_paid,
            "purchase_open": timezone.now() <= purchase_deadline,
        },
    )


@permission_required("banquet.base")
def scan_tickets(request, banquet_pk):
    banquet = get_object_or_404(Banquet, id=banquet_pk)

    react_props = {"banquet": banquet.pk}

    return render(
        request, "banquet/scan_tickets.html", {"react_props": json.dumps(react_props)}
    )


class ParticipantsListView(GeneralMixin, ListView):
    """
    List who's been invited
    """

    template_name = "banquet/participant_list.html"

    def get_queryset(self):
        return Participant.objects.filter(banquet=self.banquet)


class ThankYouView(TemplateView):
    template_name = "banquet/thank_you.html"


@permission_required("banquet.base")
def export_participants(request, year, banquet_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, fair=fair, pk=banquet_pk)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="banquet_participants.csv"'

    writer = csv.writer(response, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerow(
        [
            "Company",
            "User",
            "Name",
            "Email",
            "Alcohol",
            "Seat",
            "Dietary restrictions",
            "Other dietary restrictions",
            "Dietary preferences",
            "invitation",
            "checked_in",
        ]
    )

    for participant in (
        Participant.objects.select_related("seat")
        .select_related("seat__table")
        .filter(banquet=banquet)
    ):
        writer.writerow(
            [
                participant.company,
                participant.user,
                participant.name,
                participant.email_address,
                participant.alcohol,
                participant.seat,
                ", ".join(str(x) for x in participant.dietary_restrictions.all()),
                participant.other_dietary_restrictions,
                participant.dietary_preference,
                "https://ais.armada.nu/banquet/" + participant.token,
                participant.ticket_scanned,
            ]
        )

    return response


@permission_required("banquet.base")
def export_afterparty(request, year, banquet_pk):
    fair = get_object_or_404(Fair, year=year)
    banquet = get_object_or_404(Banquet, pk=banquet_pk)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="afterparty_participants.csv"'
    )

    writer = csv.writer(response, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerow(["Name", "Email Sent", "Email", "Inviter"])
    for participant in AfterPartyInvitation.objects.filter(banquet=banquet):
        writer.writerow(
            [
                participant.name,
                participant.used,
                participant.email_address,
                participant.inviter,
            ]
        )

    return response
