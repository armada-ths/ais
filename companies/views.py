from slackclient import SlackClient
import csv

import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.conf import settings
from django.db.models import CharField, Q, Case, When, Value, IntegerField
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.mime.text import MIMEText
import smtplib

from math import ceil

from companies.models import (
    Company,
    CompanyAddress,
    CompanyCustomerResponsible,
    Group,
    CompanyContact,
    CompanyCustomerComment,
)
from fair.models import Fair
from recruitment.models import RecruitmentApplication
from .forms import (
    CompanyForm,
    CompanyContactForm,
    CompanyAddressForm,
    BaseCompanyAddressFormSet,
    BaseCompanyContactFormSet,
    CompanyCustomerResponsibleForm,
    GroupForm,
    CompanyCustomerCommentForm,
    StatisticsForm,
    CompanyCustomerStatusForm,
    CompanyNewOrderForm,
    CompanyEditOrderForm,
    CompanySearchForm,
    ContractExportForm,
)
from register.models import SignupContract, SignupLog
from accounting.models import Revenue, Order, Product
from people.models import Profile
from exhibitors.models import Exhibitor


def current_fair():
    return get_object_or_404(Fair, current=True)


@permission_required("companies.base")
def companies_slack_call(request, year):
    profile = get_object_or_404(Profile, user=request.user)

    phone_number = request.GET["phone_number"].strip()
    phone_number = phone_number.replace("+", "00")

    sc = SlackClient(settings.SLACK_KEY)

    sc.api_call(
        "chat.postMessage", channel=profile.slack_id, text="tel://" + phone_number
    )

    return HttpResponse("")


def groups_to_tree_list(groups, selected=None):
    groups_tree = {"selected": None, "children": {}}

    for group in groups:
        path = group.path()

        p = groups_tree

        for step in range(len(path)):
            if path[step] not in p["children"]:
                p["children"][path[step]] = {
                    "selected": None if selected is None else path[step] in selected,
                    "children": {},
                }

            p = p["children"][path[step]]

    groups_list = tree_to_list(None, groups_tree)

    groups_list.pop(0)
    groups_list.pop(0)
    groups_list.pop()

    return groups_list


def tree_to_list(k, groups_tree):
    if len(groups_tree["children"].keys()) > 0:
        o = ["open_short", k, "open"]

        for child in groups_tree["children"].keys():
            o = o + tree_to_list(
                {
                    "group": child,
                    "selected": groups_tree["children"][child]["selected"],
                },
                groups_tree["children"][child],
            )

        o.append("close")

    else:
        o = ["open_short", k, "close_short"]

    return o


def has_same_group_and_users(q1, q2):
    if not q1.group.allow_statistics or not q2.group.allow_statistics:
        return True

    if q1.group != q2.group:
        return False

    for o1 in q1.users.all():
        if o1 not in q2.users.all():
            return False

    for o2 in q2.users.all():
        if o2 not in q1.users.all():
            return False

    return True


def is_equal(q1, q2):
    for ccr1 in q1:
        found = False

        for ccr2 in q2:
            if has_same_group_and_users(ccr1, ccr2):
                found = True
                break

        if not found:
            return False

    for ccr2 in q2:
        found = False

        for ccr1 in q1:
            if has_same_group_and_users(ccr2, ccr1):
                found = True
                break

        if not found:
            return False

    return True


@permission_required("companies.base")
def statistics(request, year):
    fair = get_object_or_404(Fair, year=year)
    current_fair_groups = Group.objects.filter(fair=fair)

    form = StatisticsForm(request.POST or None)

    contracts = []
    smallest = None

    for contract in SignupContract.objects.filter(fair=fair).all():
        signatures_raw = SignupLog.objects.filter(contract=contract).order_by(
            "timestamp"
        )
        signatures = []

        i = 0
        rows = 0

        for signature in signatures_raw:
            all_responsibilities = list(
                CompanyCustomerResponsible.objects.filter(company=signature.company)
            )
            # loop to exclude previous years' responsibilities
            responsibilities = []
            for responsibility in all_responsibilities:
                if responsibility.group in current_fair_groups:
                    responsibilities.append(responsibility)

            if smallest is None or signature.timestamp < smallest:
                smallest = signature.timestamp

            add = True

            for signature_existing in signatures:
                if is_equal(signature_existing["responsibilities"], responsibilities):
                    signature_existing["count"] += 1
                    signature_existing["timestamps"].append(
                        {
                            "timestamp": signature.timestamp,
                            "count": signature_existing["count"],
                        }
                    )

                    add = False
                    break

            if add:
                signatures.append(
                    {
                        "i": i,
                        "responsibilities": responsibilities,
                        "count": 1,
                        "timestamps": [{"timestamp": signature.timestamp, "count": 1}],
                    }
                )

                i += 1

        rows += len(signatures)

        row_length = len(signatures)
        table = []

        for j in range(len(signatures)):
            for timestamp in signatures[j]["timestamps"]:
                row = {"timestamp": timestamp["timestamp"], "cells": []}

                for k in range(row_length):
                    row["cells"].append(None)

                row["cells"][j] = timestamp["count"]
                table.append(row)

            j += 1

        contracts.append(
            {
                "i": len(contracts),
                "name": contract.name,
                "signatures_count": signatures_raw.count(),
                "rows": rows,
                "signatures": signatures,
                "table": table,
            }
        )

    form.fields["date_from"].initial = smallest

    return render(
        request,
        "companies/statistics.html",
        {"fair": fair, "contracts": contracts, "form": form},
    )


@permission_required("companies.base")
def companies_list(request, year):
    form = CompanySearchForm(request.GET or None)
    num_fairs = Fair.objects.count()
    year_list = range(int(year), int(year) - int(num_fairs), -1)
    form.fields["exhibitors_year"].choices = [
        (str(year), str(year)) for year in year_list
    ]
    form.fields["exhibitors_year"].initial = str(year)
    exhibitor_year = int(form["exhibitors_year"].value() or year)
    exhibitor_fair = get_object_or_404(Fair, year=exhibitor_year)
    fair = get_object_or_404(Fair, year=year)

    all_users = []

    contracts = SignupContract.objects.filter(fair=fair)

    form.fields["contracts_positive"].queryset = contracts
    form.fields["contracts_negative"].queryset = contracts

    has_filtering = request.GET and form.is_valid()

    responsibles_list = list(
        CompanyCustomerResponsible.objects.select_related("company")
        .select_related("group")
        .filter(group__fair=fair)
        .prefetch_related("users")
    )
    responsibles = {}

    print("HELLO")

    for responsible in responsibles_list:
        users = responsible.users.all()

        for user in users:
            if user not in all_users:
                all_users.append(user)

        o = {"group": responsible.group.name, "users": users}

        if responsible.company not in responsibles:
            responsibles[responsible.company] = [o]

        else:
            responsibles[responsible.company].append(o)

    all_users.sort(key=lambda x: x.get_full_name())

    form.fields["users"].choices = [
        (user.pk, user.get_full_name()) for user in all_users
    ]

    signatures_list = []
    signatures = {}

    signatures_list = list(
        SignupLog.objects.select_related("company")
        .select_related("contract")
        .filter(contract__in=SignupContract.objects.filter(fair=fair))
    )

    for signature in signatures_list:
        if signature.company not in signatures:
            signatures[signature.company] = [signature]

        else:
            signatures[signature.company].append(signature)

    # Pagination variables
    COMPANIES_PER_PAGE = 50
    page_number = int(request.GET.get("page") or 1)

    # SQL level filtering
    total_companies = Company.objects.prefetch_related("groups", "companycontact_set")
    filtered_companies = total_companies
    exhibitors = Exhibitor.objects.select_related("company").filter(fair=exhibitor_fair)
    if has_filtering:
        if form.cleaned_data["exhibitors"] == "YES":
            filtered_companies = filtered_companies.filter(pk__in=exhibitors)
        elif form.cleaned_data["exhibitors"] == "NO":
            filtered_companies = filtered_companies.exclude(pk__in=exhibitors)
        if len(form.cleaned_data["contracts_positive"]) != 0:
            contract_signing_companies = (
                SignupLog.objects.select_related("company")
                .select_related("contract")
                .filter(contract__in=form.cleaned_data["contracts_positive"])
            )
            filtered_companies = filtered_companies.filter(
                pk__in=contract_signing_companies.values_list("company")
            )
        if len(form.cleaned_data["contracts_negative"]) != 0:
            contract_signing_companies = (
                SignupLog.objects.select_related("company")
                .select_related("contract")
                .filter(contract__in=form.cleaned_data["contracts_negative"])
            )
            filtered_companies = filtered_companies.exclude(
                pk__in=contract_signing_companies.values_list("company")
            )
        if len(form.cleaned_data["users"]) != 0:
            companies_with_sought_responsibles = (
                CompanyCustomerResponsible.objects.select_related("company")
                .select_related("group")
                .filter(group__fair=fair)
                .prefetch_related("users")
                .filter(users__in=form.cleaned_data["users"])
                .values_list("company")
            )
            filtered_companies = filtered_companies.filter(
                pk__in=companies_with_sought_responsibles
            )
        if form.cleaned_data["q"]:
            # Free text search
            search_query = form.cleaned_data["q"]

            # Name search (highest in matches on company name will appear highest in results)
            name_q = get_query(search_query, ["name"])

            # Include every CharField in Company model in search
            field_names = [
                f.name for f in Company._meta.fields if isinstance(f, CharField)
            ]
            qs = get_query(search_query, field_names)

            # Responsibles
            query = get_query(search_query, ["first_name", "last_name"])
            matched_responsibles = (
                CompanyCustomerResponsible.objects.select_related("company")
                .select_related("group")
                .filter(group__fair=fair)
                .prefetch_related("users")
                .filter(users__in=User.objects.filter(query))
                .values_list("company")
            )

            qs |= Q(pk__in=matched_responsibles)

            # Contracts
            query = get_query(search_query, ["name", "type"])
            matched_contracts = (
                SignupLog.objects.select_related("company")
                .select_related("contract")
                .filter(contract__in=SignupContract.objects.filter(query))
                .values_list("company")
            )

            qs = qs | Q(pk__in=matched_contracts)

            # Contacts
            query = get_query(
                search_query,
                [
                    "first_name",
                    "last_name",
                    "email_address",
                    "alternative_email_address",
                    "mobile_phone_number",
                    "work_phone_number",
                ],
            )

            # Enable searching for phone numbers with a leading 0 by removing it
            # (since all phone numbers in database begin with +46)
            search_query_stripped = search_query.strip()
            if search_query_stripped[0] == "0":
                query = (
                    query
                    | Q(mobile_phone_number__icontains=search_query_stripped[1:])
                    | Q(work_phone_number__icontains=search_query_stripped[1:])
                )

            matched_contacts = CompanyContact.objects.filter(query).values_list(
                "company"
            )

            qs = qs | Q(pk__in=matched_contacts)

            # Groups
            query = get_query(search_query, ["name", "name_full"])
            matched_groups = (
                Group.objects.filter(query)
                .select_related("company")
                .values_list("company")
            )
            qs |= Q(pk__in=matched_groups)

            # Apply filters, ranking matches on company name higher than matches on other fields
            filtered_companies = (
                filtered_companies.annotate(
                    rank=Case(
                        When(
                            name_q,
                            then=Value(1),
                        ),
                        When(
                            qs,
                            then=Value(2),
                        ),
                        default=Value(99),
                        output_field=IntegerField(),
                    )
                )
                .order_by("rank", "name")
                .exclude(rank=99)
            )

    companies_modified = []
    companies_current_page = filtered_companies[
        (page_number - 1) * COMPANIES_PER_PAGE : page_number * COMPANIES_PER_PAGE
    ]
    for company in companies_current_page:
        exhibitor = company in exhibitors

        companies_modified.append(
            {
                "pk": company.pk,
                "name": company.name,
                "status": None,  # TODO: fix status!
                "groups": company.groups.filter(fair=fair),
                "responsibles": (
                    responsibles[company] if company in responsibles else None
                ),
                "signatures": signatures[company] if company in signatures else None,
                "exhibitor": exhibitor,
                "show_externally": company.show_externally,
            }
        )

    total_companies = filtered_companies.count()
    return render(
        request,
        "companies/companies_list.html",
        {
            "fair": fair,
            "companies": CompanyPage(
                companies_modified,
                total_companies,
                page_number,
                ceil(total_companies / COMPANIES_PER_PAGE),
            ),
            "companies_ids": [company["pk"] for company in companies_modified],
            "form": form,
        },
    )


def normalize_query(
    query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r"\s{2,}").sub,
):
    """Splits the query string in invidual keywords, getting rid of unecessary spaces
    and grouping quoted words together.
    Example:

    normalize_query('  some random  words "with   quotes  " and   spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    """
    return [normspace(" ", (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    """Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.

    """
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


class CompanyPage:
    def __init__(self, companies, total_companies, page_number, num_pages):
        self.total_companies = total_companies
        self.num_pages = num_pages
        self.object_list = companies
        self.page = page_number

    def has_previous(self):
        return self.page > 1

    def has_next(self):
        return self.page < self.num_pages

    def previous_page_number(self):
        return self.page - 1

    def next_page_number(self):
        return self.page + 1

    def __iter__(self):
        yield from self.object_list


@permission_required("companies.base")
def companies_new(request, year):
    fair = get_object_or_404(Fair, year=year)

    form = CompanyForm(request.POST or None)

    if request.POST and form.is_valid():
        company = form.save()
        return redirect("companies_view", fair.year, company.pk)

    return render(request, "companies/companies_new.html", {"fair": fair, "form": form})


@permission_required("companies.base")
def companies_view(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    company = get_object_or_404(Company, pk=pk)

    initially_selected = []

    for responsible in CompanyCustomerResponsible.objects.filter(company=company):
        if request.user in responsible.users.all():
            initially_selected.append(responsible.group)

    form_comment = CompanyCustomerCommentForm(
        request.POST if request.POST else None, initial={"groups": initially_selected}
    )

    if request.POST and form_comment.is_valid():
        comment = form_comment.save(commit=False)
        comment.company = company
        comment.user = request.user
        comment.save()
        form_comment.save()

        form_comment = CompanyCustomerCommentForm(
            initial={"groups": initially_selected}
        )

    fairs = []

    for f in Fair.objects.all().order_by("year"):
        fairs.append(
            {
                "fair": f,
                "exhibitor": Exhibitor.objects.filter(fair=f, company=company).count()
                == 1,
            }
        )

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    return render(
        request,
        "companies/companies_view.html",
        {
            "fair": fair,
            "fairs": fairs,
            "company": company,
            "groups": company.groups.all(),
            "comments": CompanyCustomerComment.objects.filter(company=company),
            "contacts": CompanyContact.objects.filter(company=company),
            "signatures": SignupLog.objects.select_related("contract").filter(
                company=company, contract__fair=fair
            ),
            "responsibles": CompanyCustomerResponsible.objects.select_related(
                "group"
            ).filter(company=company, group__fair=fair),
            "profile": profile,
            "form_comment": form_comment,
            "has_invoice_address": company.has_invoice_address,
            "orders": Order.objects.filter(
                purchasing_company=company, product__revenue__fair=fair
            ),
        },
    )


@permission_required("companies.base")
def companies_edit_responsibles_remove(request, year, pk, responsible_group_pk):
    fair = get_object_or_404(Fair, year=year)
    company = get_object_or_404(Company, pk=pk)
    responsible_group = get_object_or_404(Group, pk=responsible_group_pk, fair=fair)
    responsible = get_object_or_404(
        CompanyCustomerResponsible, company=company, group=responsible_group
    )

    responsible.delete()

    return redirect("companies_edit", fair.year, company.pk)


@permission_required("companies.base")
def companies_details(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    company = get_object_or_404(Company, pk=pk)

    form_company_details = CompanyForm(
        request.POST if request.POST else None, instance=company
    )

    if request.POST and form_company_details.is_valid():
        form_company_details.save()
        return redirect("companies_view", fair.year, company.pk)

    return render(
        request,
        "companies/companies_details.html",
        {
            "fair": fair,
            "company": company,
            "form_company_details": form_company_details,
        },
    )


@permission_required("companies.base")
def companies_edit(request, year, pk, group_pk=None, responsible_group_pk=None):
    fair = get_object_or_404(Fair, year=year)
    company = get_object_or_404(Company, pk=pk)
    responsibles = CompanyCustomerResponsible.objects.select_related("group").filter(
        company=company, group__fair=fair
    )

    if group_pk is not None:
        group_toggle = get_object_or_404(Group, pk=group_pk, fair=fair)

        if group_toggle in company.groups.all():
            company.groups.remove(group_toggle)

        elif group_toggle.allow_companies:
            company.groups.add(group_toggle)

        company.save()

    groups_list = groups_to_tree_list(
        Group.objects.filter(fair=fair).order_by("id"), company.groups.all()
    )

    if responsible_group_pk is not None:
        responsible_group = get_object_or_404(Group, pk=responsible_group_pk, fair=fair)
        responsible = get_object_or_404(
            CompanyCustomerResponsible, company=company, group=responsible_group
        )

    else:
        responsible = None

    form_responsible = CompanyCustomerResponsibleForm(
        company,
        request.POST if request.POST.get("save_responsibilities") else None,
        instance=responsible,
    )

    users = [
        recruitment_application.user
        for recruitment_application in RecruitmentApplication.objects.filter(
            status="accepted", recruitment_period__fair=fair
        ).order_by("user__first_name", "user__last_name")
    ]

    users = [
        user
        for user in users
        if (responsible is not None and user in responsible.users.all())
        or user.has_perm("companies.base")
    ]

    form_responsible.fields["users"].choices = [
        (user.pk, user.get_full_name()) for user in users
    ]
    form_responsible.fields["group"].choices = [
        (group.pk, group.__str__())
        for group in Group.objects.filter(allow_responsibilities=True, fair=fair)
    ]

    if (
        request.POST
        and request.POST.get("save_responsibilities")
        and form_responsible.is_valid()
    ):
        form_responsible.save()
        return redirect("companies_edit", fair.year, company.pk)

    form_status = CompanyCustomerStatusForm(
        request.POST if request.POST.get("save_status") else None,
        initial={"status": None},
    )  # TODO: fix

    form_status.fields["status"].choices = [("", "---------")] + [
        (group.pk, group.__str__)
        for group in Group.objects.filter(fair=fair, allow_status=True)
    ]

    if request.POST and request.POST.get("save_status") and form_status.is_valid():
        company.status = form_status.cleaned_data["status"]
        company.save()

    return render(
        request,
        "companies/companies_edit.html",
        {
            "fair": fair,
            "company": company,
            "groups_list": groups_list,
            "responsibles": responsibles,
            "responsible": responsible,
            "form_responsible": form_responsible,
            "form_status": form_status,
        },
    )


@permission_required("companies.base")
def groups(request, year, pk=None):
    fair = get_object_or_404(Fair, year=year)
    groups_list = groups_to_tree_list(Group.objects.filter(fair=fair).order_by("id"))

    group = Group.objects.filter(pk=pk).first()

    form = GroupForm(fair, request.POST or None, instance=group)

    if request.POST and form.is_valid(group):
        group = form.save()
        return redirect("groups_list", fair.year)

    return render(
        request,
        "companies/groups.html",
        {"fair": fair, "groups_list": groups_list, "form": form, "form_group": group},
    )


@permission_required("companies.base")
def email(request, year):
    fair = get_object_or_404(Fair, year=year)
    contracts = SignupContract.objects.filter(fair=fair)
    complete_contracts = SignupContract.objects.filter(fair=fair, type="COMPLETE")
    initial_contracts = SignupContract.objects.filter(fair=fair, type="INITIAL")

    categories = [
        {
            "name": "Has signed CR",
            "help_text": "Contacts that have signed a complete registration contract.",
            "users": [],
            "missing": [],
        },
        {
            "name": "Has signed IR but not CR",
            "help_text": "Contacts that have signed an initial registration contract.",
            "users": [],
            "missing": [],
        },
        {
            "name": "Has not signed IR or CR",
            "help_text": "All contacts connected to any company which has not signed any contract for the current year.",
            "users": [],
            "missing": [],
        },
    ]

    signed_companies = []

    for contract in complete_contracts:
        complete_signatures = SignupLog.objects.filter(contract=contract)
        for signature in complete_signatures:
            signed_companies.append(signature.company)

            if signature.company_contact == None:
                categories[0]["missing"].append(signature.company)
                continue

            categories[0]["users"].append(
                {
                    "i": len(categories[0]["users"]) + 1,
                    "name": signature.company_contact.first_name
                    + " "
                    + signature.company_contact.last_name,
                    "email_address": signature.company_contact.email_address,
                }
            )

    for contract in initial_contracts:
        initial_signatures = SignupLog.objects.filter(contract=contract)
        for signature in initial_signatures:
            if signature.company not in signed_companies:
                signed_companies.append(signature.company)

                if signature.company_contact == None:
                    categories[1]["missing"].append(signature.company)
                    continue

                name = "%s %s" % (
                    signature.company_contact.first_name,
                    signature.company_contact.last_name,
                )
                email = signature.company_contact.email_address

                categories[1]["users"].append(
                    {
                        "i": len(categories[1]["users"]) + 1,
                        "name": name,
                        "email_address": email,
                    }
                )

    added_email_addresses = []

    for company in Company.objects.all():
        if company not in signed_companies:
            contacts = CompanyContact.objects.filter(company=company, active=True)
            for contact in contacts:
                if contact.email_address not in added_email_addresses:
                    added_email_addresses.append(contact.email_address)

                    if signature.company_contact == None:
                        categories[2]["missing"].append(signature.company)
                        continue

                    categories[2]["users"].append(
                        {
                            "i": len(categories[2]["users"]) + 1,
                            "name": contact.first_name + " " + contact.last_name,
                            "email_address": contact.email_address,
                        }
                    )

    return render(
        request,
        "companies/email.html",
        {"fair": fair, "categories": categories},
    )


@permission_required("companies.base")
def companies_comments_edit(request, year, pk, comment_pk):
    fair = get_object_or_404(Fair, year=year)
    company = get_object_or_404(Company, pk=pk)
    comment = get_object_or_404(CompanyCustomerComment, company=company, pk=comment_pk)

    form = CompanyCustomerCommentForm(request.POST or None, instance=comment)

    if request.POST and form.is_valid():
        form.save()
        return redirect("companies_view", fair.year, company.pk)

    return render(
        request,
        "companies/companies_comments_edit.html",
        {"fair": fair, "company": company, "form": form},
    )


@permission_required("companies.base")
def companies_comments_remove(request, year, pk, comment_pk):
    fair = get_object_or_404(Fair, year=year)
    company = get_object_or_404(Company, pk=pk)
    comment = get_object_or_404(CompanyCustomerComment, company=company, pk=comment_pk)

    comment.delete()

    return redirect("companies_view", fair.year, company.pk)


@permission_required("companies.base")
def companies_orders_new(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    company = get_object_or_404(Company, pk=pk)

    form_order = CompanyNewOrderForm(request.POST or None)

    revenues_list = []
    revenues = Revenue.objects.filter(fair=fair)

    for revenue in revenues:
        revenue_list = [revenue.name, []]

        products = Product.objects.filter(revenue=revenue)

        for product in products:
            revenue_list[1].append([product.pk, product.name])

        if len(revenue_list[1]) != 0:
            revenues_list.append(revenue_list)

    form_order.fields["product"].choices = revenues_list

    if request.POST and form_order.is_valid():
        order = form_order.save(commit=False)
        order.purchasing_company = company
        order.save()

        return redirect("companies_orders_edit", fair.year, company.pk, order.pk)

    return render(
        request,
        "companies/companies_orders_new.html",
        {
            "fair": fair,
            "company": company,
            "form_order": form_order,
            "revenues": revenues_list,
        },
    )


@permission_required("companies.base")
def companies_orders_edit(request, year, pk, order_pk):
    fair = get_object_or_404(Fair, year=year)
    company = get_object_or_404(Company, pk=pk)
    order = get_object_or_404(
        Order, pk=order_pk, purchasing_company=company, export_batch=None
    )

    form_order = CompanyEditOrderForm(request.POST or None, instance=order)

    form_order.fields["name"].widget.attrs["placeholder"] = order.product.name
    form_order.fields["quantity"].widget.attrs["max"] = order.product.max_quantity
    form_order.fields["unit_price"].widget.attrs[
        "placeholder"
    ] = order.product.unit_price

    if request.POST and form_order.is_valid():
        form_order.save()

        return redirect("companies_view", fair.year, company.pk)

    return render(
        request,
        "companies/companies_orders_edit.html",
        {
            "fair": fair,
            "company": company,
            "form_order": form_order,
            "product": order.product,
        },
    )


@permission_required("companies.base")
def companies_orders_remove(request, year, pk, order_pk):
    fair = get_object_or_404(Fair, year=year)
    company = get_object_or_404(Company, pk=pk)
    order = get_object_or_404(
        Order, pk=order_pk, purchasing_company=company, export_batch=None
    )

    order.delete()

    return redirect("companies_view", fair.year, company.pk)


@permission_required("companies.base")
def send_order_summaries(request, year):
    fair = get_object_or_404(Fair, year=year)

    user = settings.MAIL_SERVER_USERNAME
    pwd = settings.MAIL_SERVER_PASSWORD

    recipients = {}

    for company_id in request.GET.getlist("id"):
        company_id = int(company_id)

        recipients[company_id] = {
            "people": [],
        }

    for signature in (
        SignupLog.objects.select_related("company")
        .select_related("company_contact")
        .filter(contract__fair=fair, company__id__in=recipients.keys())
    ):
        recipients[signature.company.id]["people"].append(signature.company_contact)
        recipients[signature.company.id]["company"] = signature.company

    for company_id in list(recipients):
        if len(recipients[company_id]["people"]) == 0:
            del recipients[company_id]

        else:
            recipients[company_id]["people"] = list(
                set(recipients[company_id]["people"])
            )
            recipients[company_id]["orders"] = []

    for order in Order.objects.filter(
        purchasing_company__in=[recipients[x]["company"] for x in recipients],
        product__revenue__fair=fair,
    ):
        recipients[order.purchasing_company.id]["orders"].append(order)

    for company_id in list(recipients):
        if len(recipients[company_id]["orders"]) == 0:
            del recipients[company_id]

        else:
            orders_total = 0

            recipient = recipients[company_id]

            order_string = ""

            for order in recipient["orders"]:
                if order.quantity == 1:
                    if order.unit_price is None:
                        order_string += (
                            str(order.quantity)
                            + " "
                            + str(order.product.name)
                            + " for "
                            + str(order.product.unit_price)
                            + " kr\n"
                        )
                        orders_total += order.product.unit_price
                    else:
                        order_string += (
                            str(order.quantity)
                            + " "
                            + str(order.product.name)
                            + " for "
                            + str(order.unit_price)
                            + " kr\n"
                        )
                        orders_total += order.unit_price
                else:
                    if order.unit_price is None:
                        order_string += (
                            str(order.quantity)
                            + " "
                            + str(order.product.name)
                            + " for "
                            + str(order.quantity * order.product.unit_price)
                            + " kr "
                            + "("
                            + str(order.product.unit_price)
                            + " kr each)\n"
                        )
                        orders_total += order.quantity * order.product.unit_price
                    else:
                        order_string += (
                            str(order.quantity)
                            + " "
                            + str(order.product.name)
                            + " for "
                            + str(order.quantity * order.unit_price)
                            + " kr "
                            + "("
                            + str(order.unit_price)
                            + " kr each)\n"
                        )
                        orders_total += order.quantity * order.unit_price
            order_string += "\n"

            for person in recipient["people"]:
                html_message = """
			<html>
	        	<body>
	        		<style>
	        			* {
	        			  font-family: sans-serif;
	        			  font-size: 12px;
	        			}
	        		</style>
	        		<div>
	        		      Hi %s,

	        		      Here follows a summary of %s current orders for THS Armada %s. You can always view your orders at https://register.armada.nu.
	                      <br/><br/>
	                      %s
	                      <br/><br/>
	                      Total: %d kr                      
	                      <br/><br/>
	                      You will receive your invoice after the fair. If you have any special requests regarding your invoice please let us know.

	                      If you wish to make any amendments to your orders or have any questions, please contact your THS Armada contact.

	                      Best regards,

	                      The THS Armada team
	                      https://armada.nu/contact/        		
	                </div>
	        	</body>
	        </html>
			""" % (
                    person.first_name,
                    recipients[company_id]["company"].name,
                    year,
                    order_string,
                    orders_total,
                )

                email_content = """Hi %s,

Here follows a summary of %s current orders for THS Armada %s. You can always view your orders at https://register.armada.nu.
%s

Total: %d kr

You will receive your invoice after the fair. If you have any special requests regarding your invoice please let us know.

If you wish to make any amendments to your orders or have any questions, please contact your THS Armada contact.

Best regards,

The THS Armada team
https://armada.nu/contact/""" % (
                    person.first_name,
                    recipients[company_id]["company"].name,
                    year,
                    order_string,
                    orders_total,
                )

                recipients[company_id]["email_content"] = email_content

                msg = MIMEMultipart()

                message = email_content
                msg["From"] = "THS Armada <armada@ais.armada.nu>"
                msg["To"] = "%s %s <%s>" % (
                    person.first_name,
                    person.last_name,
                    person.email_address,
                )
                msg["Subject"] = "Order confirmation for THS Armada %s" % (year)
                msg["Date"] = formatdate(localtime=True)
                msg["Bcc"] = "armada@ais.armada.nu"

                msg.attach(MIMEText(message, "plain"))
                try:
                    server = smtplib.SMTP(
                        settings.MAIL_SERVER_HOST, settings.MAIL_SERVER_PORT
                    )
                    server.login(user, pwd)
                    server.sendmail(
                        msg["From"], [msg["To"], msg["Bcc"]], msg.as_string()
                    )
                    server.quit()
                    print("successfully sent the mail")
                except Exception as e:
                    print(e)
                    print("failed to send mail")

    return render(
        request,
        "companies/confirmation_email.html",
        {
            "fair": fair,
        },
    )


@permission_required("companies.base")
def contracts_export(request, year):
    fair = get_object_or_404(Fair, year=year)

    form = ContractExportForm(request.POST or None)
    form.fields["contract"].queryset = SignupContract.objects.filter(fair=fair)

    if request.POST and form.is_valid():
        signatures = (
            SignupLog.objects.select_related("company")
            .select_related("company_contact")
            .filter(contract=form.cleaned_data["contract"])
        )
        lines = []

        for company in Company.objects.all():
            if form.cleaned_data["exhibitors"] != "BOTH":
                is_exhibitor = Exhibitor.objects.filter(
                    fair=fair, company=company
                ).count()

                if is_exhibitor and form.cleaned_data["exhibitors"] == "NO":
                    continue
                if not is_exhibitor and form.cleaned_data["exhibitors"] == "YES":
                    continue

            signature = None

            for signature_candidate in signatures:
                if signature_candidate.company == company:
                    signature = signature_candidate
                    break

            if signature is None and form.cleaned_data["companies"] == "YES":
                continue

            line = [company.name]

            if signature is not None:
                line.append(signature.contract.name)
                line.append(str(signature.timestamp))
                line.append(
                    (
                        signature.company_contact.first_name
                        + " "
                        + signature.company_contact.last_name
                    )
                    if signature.company_contact.first_name is not None
                    and signature.company_contact.last_name is not None
                    else ""
                )
                line.append(
                    signature.company_contact.email_address
                    if signature.company_contact.email_address is not None
                    else ""
                )
                line.append(
                    signature.company_contact.mobile_phone_number
                    if signature.company_contact.mobile_phone_number is not None
                    else ""
                )
                line.append(
                    signature.company_contact.work_phone_number
                    if signature.company_contact.work_phone_number is not None
                    else ""
                )

            lines.append(line)

        csv = '"company","contract", "signature date","company representative","e-mail address","mobile phone number","work phone number"\n'

        for line in lines:
            csv += (
                ",".join(['"' + column.replace('"', '\\"') + '"' for column in line])
                + "\n"
            )

        response = HttpResponse(csv, content_type="text/csv; charset=utf-8")
        response["Content-Length"] = len(csv)
        response["Content-Disposition"] = (
            'attachment; filename="exported signatures.csv"'
        )

        return response

    return render(
        request, "companies/contracts_export.html", {"fair": fair, "form": form}
    )


def companies_contacts_edit(request, year, pk, contact_pk):
    fair = get_object_or_404(Fair, year=year)
    company = get_object_or_404(Company, pk=pk)
    contact = get_object_or_404(CompanyContact, company=company, pk=contact_pk)

    form = CompanyContactForm(request.POST or None, instance=contact)

    if request.POST and form.is_valid():
        form.save()
        return redirect("companies_view", fair.year, company.pk)

    return render(
        request,
        "companies/companies_contacts_edit.html",
        {"fair": fair, "company": company, "form": form},
    )
