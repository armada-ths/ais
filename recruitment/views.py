import datetime, json, pytz
import requests as r
import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.template.defaultfilters import date as date_filter
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse

from fair.models import Fair
from people.models import Profile
from companies.models import Company
from people.models import Language, Profile
from util.email import send_mail
from .models import (
    RecruitmentPeriod,
    RecruitmentApplication,
    RoleApplication,
    RecruitmentApplicationComment,
    Role,
    Programme,
    CustomFieldArgument,
    CustomFieldAnswer,
    Location,
    Slot,
)

from django.forms import modelform_factory
from django import forms
from .forms import (
    RoleApplicationForm,
    CompareForm,
    RecruitmentPeriodForm,
    RecruitmentApplicationSearchForm,
    RolesForm,
    ProfileForm,
    ProfilePictureForm,
)


def assign_roles(request, year):
    if not request.user.has_perm("recruitment.administer_roles"):
        return HttpResponseForbidden()

    # Save all roles because that will guarantee that all roles have a group
    for role in Role.objects.all():
        role.save()

    # Remove permission groups from everyone that does not have a role this year
    for application in RecruitmentApplication.objects.all().exclude(
        recruitment_period__fair__year=year, delegated_role=None
    ):
        application.user.groups.clear()
        application.user.user_permissions.clear()
    # There should be no accepted applications without a delegated role, if there is one then recruitment manager has messed up
    # But we don't want this to crash if that's case so exclude all without a delegated role
    for application in RecruitmentApplication.objects.filter(
        recruitment_period__fair__year=year, status="accepted"
    ).exclude(delegated_role=None):
        application.delegated_role.add_user_to_groups(application.user)

    return redirect("recruitment", year)


@login_required
def recruitment(request, year, template_name="recruitment/recruitment.html"):
    fair = get_object_or_404(Fair, year=year)
    # raise Exception('hello')
    recruitment_periods = RecruitmentPeriod.objects.filter(fair=fair).order_by(
        "-start_date"
    )

    roles = []

    for period in recruitment_periods:
        for role in period.recruitable_roles.all():
            roles.append(role)

    return render(
        request,
        template_name,
        {"recruitment_periods": recruitment_periods, "fair": fair},
    )


def recruitment_statistics(request, year):
    fair = get_object_or_404(Fair, year=year)

    form = CompareForm(request.POST or None)

    recruitment_periods = []

    if request.POST and form.is_valid():
        for recruitment_period in form.cleaned_data["recruitment_periods"]:
            i = 1
            applications = []

            for application in RecruitmentApplication.objects.filter(
                recruitment_period=recruitment_period
            ).order_by("submission_date"):
                if (
                    application.submission_date > recruitment_period.end_date
                    and not form.cleaned_data["include_late"]
                ):
                    continue

                applications.append(
                    {
                        "i": i,
                        "difference": (
                            application.submission_date - recruitment_period.start_date
                        ).total_seconds()
                        / 86400,
                    }
                )

                i += 1

            recruitment_periods.append(
                {"name": recruitment_period.name, "applications": applications}
            )

        table_map = {}
        i = 0

        for recruitment_period in recruitment_periods:
            j = 1

            for application in recruitment_period["applications"]:
                current_row = None

                for row in table_map:
                    if row == application["difference"]:
                        current_row = table_map[row]
                        break

                if current_row is None:
                    current_row = [None for x in range(len(recruitment_periods))]

                    table_map[application["difference"]] = current_row

                current_row[i] = j

                j += 1
            i += 1

        table = []

        for row in table_map:
            table.append({"difference": row, "cells": table_map[row]})

    else:
        table = None

    return render(
        request,
        "recruitment/statistics.html",
        {
            "fair": fair,
            "form": form,
            "recruitment_periods": (
                form.cleaned_data["recruitment_periods"] if table else None
            ),
            "table": table,
        },
    )


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timezone.timedelta(n)


import time
from django.http import JsonResponse


def interview_state_counts(request, year, pk):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    application_list = (
        recruitment_period.recruitmentapplication_set.order_by("-submission_date")
        .all()
        .prefetch_related("roleapplication_set")
    )

    ignored_application_states = ["new", "accepted", "rejected"]
    interview_count_states = [
        state
        for state in recruitment_period.state_choices()
        if state[0] not in ignored_application_states
    ]

    interview_state_count_map = {}

    for interviewer in recruitment_period.interviewers():
        interview_state_count_map[interviewer] = dict(
            [(state[0], 0) for state in interview_count_states]
        )

    for application in application_list:
        if application.interviewer:
            if not application.interviewer in interview_state_count_map:
                interview_state_count_map[application.interviewer] = dict(
                    [(state[0], 0) for state in interview_count_states]
                )

            application_state = application.state()
            if application_state in interview_state_count_map[application.interviewer]:
                interview_state_count_map[application.interviewer][
                    application_state
                ] += 1

        if application.interviewer2:
            if not application.interviewer2 in interview_state_count_map:
                interview_state_count_map[application.interviewer2] = dict(
                    [(state[0], 0) for state in interview_count_states]
                )

            application_state = application.state()
            if application_state in interview_state_count_map[application.interviewer2]:
                interview_state_count_map[application.interviewer2][
                    application_state
                ] += 1

    return JsonResponse(
        {
            "data": [
                dict(
                    [("name", interviewer.get_full_name())]
                    + [
                        (state_name, state_count)
                        for state_name, state_count in state_counts.items()
                    ]
                    + [("total", sum(state_counts.values()))]
                )
                for interviewer, state_counts in interview_state_count_map.items()
            ]
        }
    )


def recruitment_period_graphs(request, year, pk):
    start = time.time()
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    application_list = (
        recruitment_period.recruitmentapplication_set.order_by("-submission_date")
        .all()
        .prefetch_related("roleapplication_set")
    )

    # Graph stuff :)
    class ValueCounter(object):
        def __init__(self, description, monocolor, charts, values=None, sort_key=None):
            self.data = {}
            self.description = description
            self.monocolor = monocolor
            self.charts = charts
            self.sort_key = sort_key
            self.y_limit = None

            if values:
                self.add_values(values)

        def add_value(self, value):
            if not value in self.data:
                self.data[value] = 0
            self.data[value] += 1

        def add_values(self, values):
            for value in values:
                self.add_value(value)

        def sorted_values(self):
            return sorted(self.data.keys(), key=self.sort_key)

        def sorted_value_counts(self):
            return [self.data[key] for key in self.sorted_values()]

        def json(self):
            return {
                "description": self.description,
                "monocolor": self.monocolor,
                "charts": self.charts,
                "sorted_values": self.sorted_values(),
                "sorted_value_counts": self.sorted_value_counts(),
                "y_limit": self.y_limit,
            }

    date_dictionary = dict(
        [
            (
                date_filter(application.submission_date, "d M"),
                application.submission_date,
            )
            for application in application_list
        ]
    )
    applications_per_date_count = ValueCounter(
        "Applications per date",
        True,
        ["bar"],
        [
            date_filter(application.submission_date, "d M")
            for application in application_list
        ],
        lambda x: date_dictionary[x],
    )

    role_applications = RoleApplication.objects.filter(
        recruitment_application__recruitment_period=recruitment_period
    ).prefetch_related("role")

    total_role_application_count = ValueCounter(
        "Total number of applications per role",
        False,
        ["bar", "pie"],
        [role_application.role.name for role_application in role_applications],
    )

    first_preference_role_application_count = ValueCounter(
        "Number of first preference applications per role",
        False,
        ["bar", "pie"],
        [
            role_application.role.name
            for role_application in role_applications.filter(order=0)
        ],
    )

    # Add graphs also for application questions where users select from a fixed set of arguments
    custom_field_counts = []
    for custom_field in recruitment_period.application_questions.customfield_set.all():
        try:
            arguments = custom_field.customfieldargument_set.all()
            if len(arguments) > 0:
                custom_field_count = ValueCounter(
                    custom_field.question,
                    False,
                    ["bar"],
                    [
                        arguments.get(pk=int(answer.answer)).value
                        for answer in custom_field.customfieldanswer_set.all()
                    ],
                )
                custom_field_counts.append(custom_field_count)

                # Also, for each argument we want to plot bar graphs so we can see the number of english or swedish applicants per date
                argument_per_date_counts = []
                y_limit = 0
                for argument in arguments:
                    date_dictionary = dict(
                        [
                            (
                                date_filter(application.submission_date, "d M"),
                                application.submission_date,
                            )
                            for application in application_list
                        ]
                    )

                    argument_per_date_count = ValueCounter(
                        argument.value,
                        True,
                        ["bar"],
                        [
                            date_filter(application.submission_date, "d M")
                            for application in application_list
                            if CustomFieldAnswer.objects.filter(
                                user=application.user, answer=str(argument.pk)
                            ).exists()
                        ],
                        lambda x: date_dictionary[x],
                    )

                    for date in daterange(
                        recruitment_period.start_date,
                        min(timezone.now(), recruitment_period.end_date),
                    ):
                        date_string = date_filter(date, "d M")
                        if not date_string in argument_per_date_count.data:
                            argument_per_date_count.data[date_string] = 0
                            date_dictionary[date_string] = date

                    y_limit = max(y_limit, max(argument_per_date_count.data.values()))
                    argument_per_date_counts.append(argument_per_date_count)

                for argument_per_date_count in argument_per_date_counts:
                    argument_per_date_count.y_limit = y_limit
                    custom_field_counts.append(argument_per_date_count)

        except (ValueError, ObjectDoesNotExist):
            pass

    def user_has_programme(user):
        try:
            return user.profile
        except ObjectDoesNotExist:
            return False

    programme_applications_count = ValueCounter(
        "Applications per programme",
        True,
        ["bar"],
        [
            application.user.profile.programme.name
            for application in application_list.prefetch_related(
                "user", "user__profile", "user__profile__programme"
            )
            if user_has_programme(application.user)
            and application.user.profile.programme
        ],
    )

    value_counters = [
        applications_per_date_count,
        total_role_application_count,
        first_preference_role_application_count,
        programme_applications_count,
    ] + custom_field_counts

    return JsonResponse(
        {"graph_datasets": [value_counter.json() for value_counter in value_counters]}
    )


from django.http import HttpResponseRedirect
import urllib


def remember_last_query_params(url_name, query_params):
    """Stores the specified list of query params from the last time this user
    looked at this URL (by url_name). Stores the last values in the session.
    If the view is subsequently rendered w/o specifying ANY of the query params,
    it will redirect to the same URL with the last query params added to the URL.

    url_name is a unique identifier key for this view or view type if you want
    to group multiple views together in terms of shared history

    Example:

    @remember_last_query_params("jobs", ["category", "location"])
    def myview(request):
            pass

    """

    def is_query_params_specified(request, query_params):
        """Are any of the query parameters we are interested in on this request URL?"""
        for current_param in request.GET:
            if current_param in query_params:
                return True
        return False

    def params_from_last_time(request, key_prefix, query_params):
        """Gets a dictionary of JUST the params from the last render with values"""
        params = {}
        for query_param in query_params:
            last_value = request.session.get(key_prefix + query_param)
            if last_value:
                params[query_param] = last_value
        return params

    def update_url(url, params):
        """update an existing URL with or without paramters to include new parameters
        from http://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python
        """
        if not params:
            return url
        if not url:  # handle None
            url = ""
        url_parts = list(urllib.parse.urlparse(url))
        # http://docs.python.org/library/urlparse.html#urlparse.urlparse, part 4 == params
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urllib.parse.urlencode(query)
        return urllib.parse.urlunparse(url_parts)

    def do_decorator(view_func):
        def decorator(*args, **kwargs):
            request = args[0]

            key_prefix = url_name + "_"

            if is_query_params_specified(request, query_params):
                for query_param in query_params:
                    request.session[key_prefix + query_param] = request.GET.get(
                        query_param
                    )

            else:
                last_params = params_from_last_time(request, key_prefix, query_params)
                if last_params and last_params != {}:
                    current_url = "%s?%s" % (
                        request.META.get("PATH_INFO"),
                        request.META.get("QUERY_STRING"),
                    )
                    new_url = update_url(current_url, last_params)
                    return HttpResponseRedirect(new_url)

            return view_func(*args, **kwargs)

        return decorator

    return do_decorator


@remember_last_query_params(
    "recruitment", [field for field in RecruitmentApplicationSearchForm().fields]
)
def recruitment_period(
    request, year, pk, template_name="recruitment/recruitment_period.html"
):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    eligible_roles = recruitment_period.eligible_roles

    # We should be able to trust eligible_roles in the model,
    # but in case something goes awry.
    if eligible_roles < 1:
        eligible_roles = 1

    fair = get_object_or_404(Fair, year=year)
    start = time.time()

    sort_field = request.GET.get("sort_field")
    if not sort_field:
        sort_field = "submission_date"
    sort_ascending = request.GET.get("sort_ascending") == "true"

    order_by_query = ("" if sort_ascending else "-") + sort_field

    application_list = (
        recruitment_period.recruitmentapplication_set.order_by(
            order_by_query, "-submission_date"
        )
        .all()
        .prefetch_related("roleapplication_set")
    )
    # user should be forbidden to look at applications that are not below them in hierari
    # application_list = list(filter(lambda application: eligible_to_see_application(application, user), application_list))

    search_form = RecruitmentApplicationSearchForm(request.GET or None)
    search_form.fields["role"].choices = [("", "---------")] + [
        (role.pk, role.name) for role in recruitment_period.recruitable_roles.all()
    ]
    search_form.fields["priority"].choices = [("", "-------")] + [
        (str(i), str(i + 1) + ":" + ("st" if i == 0 else "nd" if i == 1 else "rd"))
        for i in range(eligible_roles)
    ]
    search_form.fields["interviewer"].choices = [("", "---------")] + [
        (interviewer.pk, interviewer.get_full_name())
        for interviewer in recruitment_period.interviewers()
    ]
    search_form.fields["recommended_role"].choices = [("", "---------")] + [
        (role.pk, role.name) for role in recruitment_period.recruitable_roles.all()
    ]
    search_form.fields["state"].choices = [
        ("", "-------")
    ] + recruitment_period.state_choices()

    if search_form.is_valid():
        application_list = search_form.applications_matching_search(application_list)

    administrator_access = user_can_access_recruitment_period(
        request.user, recruitment_period
    )

    number_of_applications_per_page = 25
    paginator = Paginator(application_list, number_of_applications_per_page)
    page = request.GET.get("page")
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        applications = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        applications = paginator.page(paginator.num_pages)

    class SearchField(object):
        def __init__(self, name, model_field_name):
            self.name = name
            self.model_field_name = model_field_name

    search_fields = [
        SearchField("Name", "user__last_name"),
        SearchField("Programme", "user__profile__programme"),
        SearchField("Submitted", "submission_date"),
        SearchField("Role", None),
        SearchField("Priority", None),
        SearchField("Interviewer", "interviewer__last_name"),
        SearchField("Recommended role", "recommended_role"),
        SearchField("Rating", "rating"),
        SearchField("State", None),
    ]

    profile = Profile.objects.filter(user=request.user).first()
    token = profile.token if profile is not None else None

    return render(
        request,
        template_name,
        {
            "recruitment_period": recruitment_period,
            "application": recruitment_period.recruitmentapplication_set.filter(
                user=request.user
            ).first(),
            "interviews": (
                recruitment_period.recruitmentapplication_set.filter(
                    interviewer=request.user
                )
                | recruitment_period.recruitmentapplication_set.filter(
                    interviewer2=request.user
                )
                | recruitment_period.recruitmentapplication_set.filter(
                    user=request.user
                )
            ).all(),
            "paginator": paginator,
            "applications": applications,
            "now": timezone.now(),
            "search_form": search_form,
            "search_fields": search_fields,
            "fair": fair,
            "administrator_access": administrator_access,
            "user": request.user,
            "token": token,
        },
    )


def recruitment_period_export(
    request, year, pk, template_name="recruitment/recruitment_period_export.html"
):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    applications = RecruitmentApplication.objects.filter(
        recruitment_period=recruitment_period
    ).prefetch_related("user")

    return render(request, template_name, {"applications": applications})


def recruitment_period_email(
    request, year, pk, template_name="recruitment/recruitment_period_email.html"
):
    fair = get_object_or_404(Fair, year=year)
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    applications = RecruitmentApplication.objects.filter(
        recruitment_period=recruitment_period
    ).prefetch_related("user")

    categories = []

    for application in applications:
        category_current = None

        for category in categories:
            if category["name"] == application.status:
                category_current = category
                break

        if category_current is None:
            category_current = {"name": application.status, "users": []}
            categories.append(category_current)

        category_current["users"].append(
            {
                "i": len(category_current["users"]) + 1,
                "name": application.user.first_name + " " + application.user.last_name,
                "email_address": application.user.email,
            }
        )

    return render(
        request,
        template_name,
        {
            "fair": fair,
            "recruitment_period": recruitment_period,
            "categories": categories,
        },
    )


def recruitment_period_locations(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    applications = (
        RecruitmentApplication.objects.select_related("slot")
        .filter(recruitment_period=recruitment_period)
        .exclude(slot=None)
    )

    used_slots = {}

    for application in applications:
        if application.slot not in used_slots:
            used_slots[application.slot] = []
        used_slots[application.slot].append(
            application
        )  # creating a list of all applications connected to each slot

    locations = {}
    slots = Slot.objects.select_related("location").filter(
        recruitment_period=recruitment_period
    )

    for location in Location.objects.all():
        locations[location] = []

    for slot in slots:
        locations[slot.location].append(
            {
                "slot": slot,
                "interviews": (
                    used_slots[slot] if slot in used_slots else None
                ),  # note that interviews is a list of all interviews for a slot
            }
        )

    locations_list = []
    j = 0

    local_tz = pytz.timezone("Europe/Stockholm")

    for location in locations:
        location_modified = {
            "i": j,
            "name": location.name,
            "slots": locations[location],
        }

        j += 1

        date_modified_previous = None

        for i in range(len(location_modified["slots"])):
            date = local_tz.localize(
                location_modified["slots"][i]["slot"].start, is_dst=None
            )

            time_start = date.strftime("%H:%M")

            time_end = date + datetime.timedelta(minutes=slot.length)
            time_end = time_end.strftime("%H:%M")

            date_modified = date.strftime("%Y-%m-%d")

            location_modified["slots"][i] = {
                "date": (
                    date_modified if date_modified_previous != date_modified else None
                ),
                "rowspawn": None,
                "time_start": time_start,
                "time_end": time_end,
                "interviews": location_modified["slots"][i]["interviews"],
            }

            date_modified_previous = date_modified

        c = 1

        for i in reversed(range(len(location_modified["slots"]))):
            if location_modified["slots"][i]["date"] is not None:
                if c > 1:
                    location_modified["slots"][i]["rowspan"] = c
                c = 1

            else:
                c += 1

        if c > 1:
            location_modified["slots"][0]["rowspan"] = c

        locations_list.append(location_modified)

    return render(
        request,
        "recruitment/recruitment_period_locations.html",
        {
            "fair": fair,
            "recruitment_period": recruitment_period,
            "locations": locations_list,
        },
    )


def recruitment_period_delete(request, year, pk):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)

    if not user_can_access_recruitment_period(request.user, recruitment_period):
        return HttpResponseForbidden()

    recruitment_period.delete()
    return redirect("recruitment", year)


def recruitment_period_edit(request, year, pk=None):
    recruitment_period = RecruitmentPeriod.objects.filter(pk=pk).first()

    if pk != None:
        if not user_can_access_recruitment_period(request.user, recruitment_period):
            return HttpResponseForbidden()
    else:
        if not request.user.has_perm("recruitment.add_recruitmentperiod"):
            return HttpResponseForbidden()

    fair = get_object_or_404(Fair, year=year)
    form = RecruitmentPeriodForm(request.POST or None, instance=recruitment_period)

    if request.POST:
        if form.is_valid():
            recruitment_period = form.save(commit=False)
            recruitment_period.fair = fair
            recruitment_period.save()
            recruitment_period.interview_questions.handle_questions_from_request(
                request, "interview_questions"
            )
            recruitment_period.application_questions.handle_questions_from_request(
                request, "application_questions"
            )

            recruitment_period.save()

            return redirect("recruitment_period", year=year, pk=recruitment_period.id)

    return render(
        request,
        "recruitment/recruitment_period_new.html",
        {
            "form": form,
            "recruitment_period": recruitment_period,
            "interview_questions": (
                []
                if not recruitment_period
                else recruitment_period.interview_questions.customfield_set.all()
            ),
            "application_questions": (
                []
                if not recruitment_period
                else recruitment_period.application_questions.customfield_set.all()
            ),
            "fair": fair,
        },
    )


def roles_new(request, year, pk=None, template_name="recruitment/roles_form.html"):
    fair = get_object_or_404(Fair, year=year)
    role = Role.objects.filter(pk=pk).first()
    roles_form = RolesForm(request.POST or None, instance=role)

    if request.user.has_perm("recruitment.administer_roles"):
        if roles_form.is_valid():
            roles_form.save()
            return redirect("recruitment", fair.year)

    users = [
        application.user
        for application in RecruitmentApplication.objects.filter(
            delegated_role=role, status="accepted"
        )
    ]
    return render(
        request,
        template_name,
        {"role": role, "users": users, "roles_form": roles_form, "fair": fair},
    )


@permission_required("recruitment.administer_roles", raise_exception=True)
def roles_delete(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    role = get_object_or_404(Role, pk=pk)
    role.delete()
    return redirect("recruitment", fair.year)


def recruitment_application_comment_new(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    comment = RecruitmentApplicationComment()
    comment.user = request.user
    comment.recruitment_application = application
    comment.comment = request.POST["comment"]
    comment.save()
    return redirect(
        "recruitment_application_interview",
        fair.year,
        application.recruitment_period.pk,
        application.id,
    )


def recruitment_application_new(
    request,
    year,
    recruitment_period_pk,
    pk=None,
    template_name="recruitment/recruitment_application_new.html",
):
    fair = get_object_or_404(Fair, year=year)
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=recruitment_period_pk)

    if not pk:
        recruitment_application = recruitment_period.recruitmentapplication_set.filter(
            user=request.user
        ).first()

        # If the user already has an application for this period redirect to it
        if recruitment_application:
            return redirect(
                "recruitment_application_new",
                fair.year,
                recruitment_period.pk,
                recruitment_application.pk,
            )

    recruitment_application = RecruitmentApplication.objects.filter(pk=pk).first()

    user = recruitment_application.user if recruitment_application else request.user
    profile = Profile.objects.filter(user=user).first()
    if not profile:
        p = Profile(user=user)
        p.save()

    now = timezone.now()

    if recruitment_period.start_date > now:
        return render(
            request,
            "recruitment/recruitment_application_closed.html",
            {
                "recruitment_period": recruitment_period,
                "message": "Application has not opened",
                "fair": fair,
            },
        )

    if recruitment_period.end_date < now:
        return render(
            request,
            "recruitment/recruitment_application_closed.html",
            {
                "recruitment_period": recruitment_period,
                "message": "Application closed",
                "fair": fair,
            },
        )

    profile_form = ProfileForm(
        request.POST or None, request.FILES or None, instance=profile
    )

    role_form = RoleApplicationForm(request.POST or None)

    for i in range(1, 4):
        key = "role%d" % i
        role_form.fields[key].queryset = recruitment_period.recruitable_roles
        if recruitment_application:
            role_application = RoleApplication.objects.filter(
                recruitment_application=recruitment_application, order=i - 1
            ).first()
            if role_application:
                role_form.fields[key].initial = role_application.role.pk

    message_to_applicants = recruitment_period.message_to_applicants

    if request.POST:
        recruitment_period.application_questions.handle_answers_from_request(
            request, user
        )
        if role_form.is_valid() and profile_form.is_valid():
            if not recruitment_application:
                recruitment_application = RecruitmentApplication()
                send_confirmation_email(request, user, recruitment_period)

            recruitment_application.user = user
            recruitment_application.recruitment_period = recruitment_period
            recruitment_application.save()

            recruitment_application.roleapplication_set.all().delete()
            for i in range(1, 4):
                key = "role%d" % i
                role = role_form.cleaned_data[key]
                if role:
                    RoleApplication.objects.create(
                        recruitment_application=recruitment_application,
                        role=role,
                        order=i - 1,
                    )

            if pk == None:  # Slack webhook for signup notifications
                r.post(
                    settings.RECRUITMENT_HOOK_URL,
                    data=json.dumps(
                        {
                            "text": " {!s} {!s} just applied for {!s}!".format(
                                user.first_name,
                                user.last_name,
                                role_form.cleaned_data["role1"],
                            )
                        }
                    ),
                )

            profile_form.save()
            return redirect("recruitment_period", fair.year, recruitment_period.pk)

    return render(
        request,
        template_name,
        {
            "application_questions_with_answers": recruitment_period.application_questions.questions_with_answers_for_user(
                recruitment_application.user if recruitment_application else None
            ),
            "recruitment_period": recruitment_period,
            "profile_form": profile_form,
            "profile": profile,
            "role_form": role_form,
            "new_application": pk == None,
            "fair": fair,
            "message_to_applicants": message_to_applicants,
        },
    )


def get_recruiter_information(fair):
    roles = ["Head of Human Resources", "Project Manager"]
    for role in roles:
        for applicant in RecruitmentApplication.objects.filter(
            status="accepted",
            delegated_role__name=role,
            recruitment_period__fair=fair,
        ).all():
            hr_profile = create_profile(applicant)
            if hr_profile is not None:
                return hr_profile

    return {
        "name": "Armada",
        "role": "support",
        "email": "recruitment@armada.nu",
    }


def send_confirmation_email(request, user, recruitment_period):
    hr_profile = get_recruiter_information(recruitment_period.fair)
    url_to_application = "https://ais.armada.nu/fairs/%s/recruitment/%s" % (
        str(recruitment_period.fair.year),
        str(recruitment_period.pk),
    )

    send_mail(
        request,
        template="register/email/received_application.html",
        context={
            "user": user,
            "recruitment_period": recruitment_period,
            "url_to_application": url_to_application,
            "hr_name": hr_profile.get("name"),
            "hr_role": hr_profile.get("role"),
            "hr_email": hr_profile.get("email"),
        },
        subject="Thank you for applying to THS Armada!",
        to=[user.email],
    )


def create_profile(applicant):
    profile = Profile.objects.filter(user=applicant.user).first()
    return {
        "name": profile if profile else None,
        "role": applicant.delegated_role.name if applicant else None,
        "email": "recruitment@armada.nu",
    }


def set_foreign_key_from_request(request, model, model_field, foreign_key_model):
    if model_field in request.POST:
        try:
            foreign_key_id = int(request.POST[model_field])
            role = foreign_key_model.objects.filter(id=foreign_key_id).first()
            setattr(model, model_field, role)
            model.save()
        except ValueError:
            setattr(model, model_field, None)
            model.save()


def set_int_key_from_request(request, model, model_field):
    if model_field in request.POST:
        try:
            setattr(model, model_field, int(request.POST[model_field]))
            model.save()
        except ValueError:
            setattr(model, model_field, None)
            model.save()


def set_string_key_from_request(request, model, model_field):
    if model_field in request.POST:
        try:
            setattr(model, model_field, request.POST[model_field])
            model.save()
        except (ValueError, ValidationError) as e:
            setattr(model, model_field, None)
            model.save()


def set_image_key_from_request(request, model, model_field, file_directory):
    image_key = model_field
    if image_key in request.FILES:
        try:
            file = request.FILES[image_key]
            file_extension = file.name.split(".")[-1]
            if file_extension in ["png", "jpg", "jpeg"]:
                file_path = "%s/%d/image.%s" % (
                    file_directory,
                    model.pk,
                    file_extension,
                )
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)
                default_storage.save(file_path, ContentFile(file.read()))
                setattr(model, model_field, file_path)
                model.save()
        except (ValueError, ValidationError) as e:
            setattr(model, model_field, None)
            model.save()


def recruitment_application_interview(
    request,
    year,
    recruitment_period_pk,
    pk,
    template_name="recruitment/recruitment_application_interview.html",
):
    fair = get_object_or_404(Fair, year=year)
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    user = request.user

    if not user_can_access_recruitment_period(user, application.recruitment_period):
        return HttpResponseForbidden()

    InterviewPlanningForm = modelform_factory(
        RecruitmentApplication,
        fields=(
            "interviewer",
            "interviewer2",
            "slot",
            "recommended_role",
            "scorecard",
            "drive_document",
            "rating",
        ),
        widgets={
            "rating": forms.Select(
                choices=[("", "-------"), (1, 1), (2, 2), (3, 3), (5, 5)]
            ),
            "scorecard": forms.TextInput(
                attrs={"placeholder": "Link to existing document"}
            ),
            "drive_document": forms.TextInput(
                attrs={"placeholder": "Link to existing document"}
            ),
        },
        labels={
            "drive_document": _("Interview document"),
        },
        help_texts={
            "slot": "<strong>Note:</strong> If you select a slot with <strong>Other</strong> as the location you must book a location separately and communicate this location to the participants of the interview."
        },
    )

    profile_pic_form = None
    profile = Profile.objects.get(user=application.user)

    if Profile.objects.filter(user=application.user).first():
        profile_pic_form = ProfilePictureForm(
            request.POST or None, request.FILES or None, instance=profile
        )

    interviewers = application.recruitment_period.interviewers()
    interview_planning_form = InterviewPlanningForm(
        request.POST or None, instance=application
    )
    interview_planning_form.fields[
        "recommended_role"
    ].queryset = application.recruitment_period.recruitable_roles

    used_slots = []

    for a in (
        RecruitmentApplication.objects.select_related("slot")
        .exclude(slot=None)
        .exclude(pk=application.pk)
    ):
        used_slots.append(a.slot)

    slots_by_day = [("", "---------")]
    all_slots = Slot.objects.filter(recruitment_period=application.recruitment_period)

    local_tz = pytz.timezone("Europe/Stockholm")

    for slot in all_slots:
        found = False

        slot_yyyymmdd = local_tz.localize(slot.start, is_dst=None)
        slot_yyyymmdd = slot_yyyymmdd.strftime("%Y-%m-%d")

        for slot_by_day in slots_by_day:
            if slot_by_day[0] == slot_yyyymmdd:
                found = True
                break

        if not found:
            slots_by_day.append((slot_yyyymmdd, []))

    for slot in all_slots:
        if slot in used_slots and slot.location.name != "Other":
            continue

        slot_start = local_tz.localize(slot.start, is_dst=None)
        slot_yyyymmdd = slot_start.strftime("%Y-%m-%d")

        for slot_by_day in slots_by_day:
            if slot_by_day[0] == slot_yyyymmdd:
                slot_hhmm_start = slot_start.strftime("%H:%M")

                slot_hhmm_end = slot_start + datetime.timedelta(minutes=slot.length)
                slot_hhmm_end = slot_hhmm_end.strftime("%H:%M")

                slot_by_day[1].append(
                    (
                        slot.pk,
                        slot_hhmm_start
                        + "-"
                        + slot_hhmm_end
                        + " | "
                        + str(slot.location),
                    )
                )
                break

    interview_planning_form.fields["slot"].choices = slots_by_day

    languages = Language.objects.all()
    interviewers_by_language = [(None, [])]

    for language in languages:
        interviewers_by_language.insert(0, (language, []))

    for interviewer in interviewers:
        p = Profile.objects.filter(user=interviewer).first()

        for language in interviewers_by_language:
            if language[0] == p.preferred_language:
                language[1].append((interviewer.pk, interviewer.get_full_name()))
                break

    interviewers_by_language[len(interviewers_by_language) - 1] = (
        "No preferred language",
        interviewers_by_language[len(interviewers_by_language) - 1][1],
    )

    interviewers_by_language = [x for x in interviewers_by_language if len(x[1]) > 0]

    interviewers_by_language.insert(0, ("", "---------"))

    if "interviewer" in interview_planning_form.fields:
        interview_planning_form.fields["interviewer"].choices = interviewers_by_language
    if "interviewer2" in interview_planning_form.fields:
        interview_planning_form.fields[
            "interviewer2"
        ].choices = interviewers_by_language

    RoleDelegationForm = modelform_factory(
        RecruitmentApplication, fields=["delegated_role", "superior_user", "status"]
    )

    role_delegation_form = RoleDelegationForm(
        request.POST or None, instance=application
    )
    role_delegation_form.fields[
        "delegated_role"
    ].queryset = application.recruitment_period.recruitable_roles
    role_delegation_form.fields["superior_user"].choices = [("", "---------")] + [
        (interviewer.pk, interviewer.get_full_name()) for interviewer in interviewers
    ]

    if request.POST:
        application.recruitment_period.interview_questions.handle_answers_from_request(
            request, application.user
        )

        if interview_planning_form.is_valid():
            interview_planning_form.save()

            if role_delegation_form:
                if role_delegation_form.is_valid():
                    role_delegation_form.save()
                    return redirect(
                        "recruitment_period",
                        fair.year,
                        application.recruitment_period.pk,
                    )
            else:
                return redirect(
                    "recruitment_period", fair.year, application.recruitment_period.pk
                )

    if (
        application.slot
        and application.interviewer
        and application.interviewer2
        and (
            request.user == application.interviewer
            or request.user == application.interviewer2
        )
    ):
        other = (
            application.interviewer
            if application.interviewer != request.user
            else application.interviewer2
        )

        nicetime = local_tz.localize(slot.start, is_dst=None)
        nicetime = nicetime.strftime("%Y-%m-%d %H:%M")

        sms_english = (
            "Hello! Thank you for applying to THS Armada. This is a confirmation of our interview arrangement. The interview is scheduled to take place on "
            + nicetime
            + " in "
            + str(slot.location)
            + ". If you have any questions or if you would like to change the date and time, don't hesitate to contact me. "
            + other.first_name
            + " "
            + other.last_name
            + " and I are looking forward to meet you. /"
            + request.user.first_name
            + " "
            + request.user.last_name
        )

        sms_swedish = (
            "Hej! Tack för att du har sökt till THS Armada. Detta är en bekräftelse på vår överenskommelse. Intervjun är planerad till "
            + nicetime
            + " i "
            + str(slot.location)
            + ". Tveka inte att kontakta mig om du har några frågor eller om du vill ändra datum eller tid. "
            + other.first_name
            + " "
            + other.last_name
            + " och jag själv ser fram emot att få träffa dig. /"
            + request.user.first_name
            + " "
            + request.user.last_name
        )

    elif (
        application.slot
        and application.interviewer
        and request.user == application.interviewer
    ):
        nicetime = local_tz.localize(slot.start, is_dst=None)
        nicetime = nicetime.strftime("%Y-%m-%d %H:%M")

        sms_english = (
            "Hello! Thank you for applying to THS Armada. This is a confirmation of our interview arrangement. The interview is scheduled to take place on "
            + nicetime
            + " in "
            + str(slot.location)
            + ". If you have any questions or if you would like to change the date and time, don't hesitate to contact me. I am looking forward to meet you. /"
            + request.user.first_name
            + " "
            + request.user.last_name
        )

        sms_swedish = (
            "Hej! Tack för att du har sökt till THS Armada. Detta är en bekräftelse på vår överenskommelse. Intervjun är planerad till "
            + nicetime
            + " i "
            + str(slot.location)
            + ". Tveka inte att kontakta mig om du har några frågor eller om du vill ändra datum eller tid. Jag ser fram emot att få träffa dig. /"
            + request.user.first_name
            + " "
            + request.user.last_name
        )

    else:
        sms_english = None
        sms_swedish = None

    return render(
        request,
        template_name,
        {
            "profile_pic_form": profile_pic_form,
            "application": application,
            "application_questions_with_answers": application.recruitment_period.application_questions.questions_with_answers_for_user(
                application.user
            ),
            "interview_questions_with_answers": application.recruitment_period.interview_questions.questions_with_answers_for_user(
                application.user
            ),
            "interview_planning_form": interview_planning_form,
            "role_delegation_form": role_delegation_form,
            "profile": profile,
            "sms_english": sms_english,
            "sms_swedish": sms_swedish,
            "fair": fair,
        },
    )


@permission_required("recruitment.delete_recruitmentapplication")
def recruitment_application_delete(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    recruitment_application = get_object_or_404(RecruitmentApplication, pk=pk)
    recruitment_application.delete()
    return redirect(
        "recruitment_period", fair.year, recruitment_application.recruitment_period.pk
    )


def user_can_access_recruitment_period(user, recruitment_period):
    if user.is_superuser:
        return True

    if (
        len(user.groups.all().intersection(recruitment_period.allowed_groups.all()))
        != 0
    ):
        return True

    # for group in user.groups.all():
    #    if group in recruitment_period.allowed_groups.all():
    #        return True

    return False


def export_applications(request, year, pk):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    if not user_can_access_recruitment_period(request.user, recruitment_period):
        return HttpResponseForbidden()
    applications = RecruitmentApplication.objects.filter(
        recruitment_period=recruitment_period
    )
    txt = "SEP=, \n"
    response = HttpResponse(txt, content_type="text/csv")
    response["Content-Length"] = len(txt)
    response["Content-Disposition"] = 'attachment; filename="exported_applications.csv"'
    writer = csv.writer(response)
    writer.writerow(["Name", "E-mail", "Roles applied for", "Team1", "Team2", "Team3"])
    for application in applications:
        applicationsArray = []
        applicationsArray.append(str(application.user))
        applicationsArray.append(str(application.user.email))
        rolesArray = []
        for role in application.roles:
            rolesArray.append(role.role.name)
        allRoles = " & ".join(rolesArray)
        applicationsArray.append(allRoles)
        writer.writerow(applicationsArray)
    return response
