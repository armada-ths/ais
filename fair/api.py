import operator
from functools import reduce
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.db.models import Q, Subquery, OuterRef
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from django.http import QueryDict
from fair import serializers
from fair.models import (
    Fair,
    LunchTicket,
    LunchTicketScan,
    LunchTicketTime,
    FairDay,
)

from accounting.models import Order, Product, Category, ChildProduct
from companies.models import Company, CompanyContact
from people.models import DietaryRestriction
from .forms import LunchTicketForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
import json
from django.db import transaction

from util import (
    JSONError,
    get_company_contact,
    get_contract_signature,
    get_fair,
    get_user,
    status,
)


@require_GET
def lunchtickets_search(request):
    """
    Search lunch tickets for the current fair
    """

    fair = Fair.objects.get(current=True)
    search_query = request.GET.get("query", "")

    if search_query == "":
        return JsonResponse({"message": "Query is empty."}, status=400)

    names = search_query.split()

    name_query = reduce(
        operator.__or__,
        [
            Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)
            for query in names
        ],
    )

    lunch_tickets = LunchTicket.objects.filter(
        Q(fair=fair)
        & (
            Q(company__name__icontains=search_query)
            | Q(email_address__icontains=search_query)
            | name_query
        )
    ).all()

    data = {
        "result": [
            serializers.lunch_ticket(lunch_ticket) for lunch_ticket in lunch_tickets
        ]
    }

    return JsonResponse(data, safe=False)


def company_total_lunch_tickets(fair: Fair, company_name: str):
    """
    Given a specific company get all unassigned lunch tickets,
    meaning the total amount of tickets the company bought minus
    the amount of tickets that they have already created.
    """

    already_created_lunch_tickets = LunchTicket.objects.filter(
        fair=fair, company__name__exact=company_name
    ).all()

    # TODO Document this hardcoded query (relation to the category "Lunch Ticket")
    lunch_ticket_categories = Category.objects.filter(
        fair=fair, name__icontains="Lunch Ticket"  # Not case sensitive
    ).all()

    lunch_ticket_products = Product.objects.filter(
        category__in=lunch_ticket_categories
    ).all()  # Fetch all products that contain the category "[current_year]Lunch Ticket"

    company = Company.objects.filter(name__exact=company_name).values("id").first()
    # This list contains all the addition tickets that have been bought by the company this year
    lunch_ticket_orders = Order.objects.filter(
        product__in=lunch_ticket_products, purchasing_company__exact=company["id"]
    )

    # Let's count tickets
    company_tickets = 0

    # Go through result and for each result get the quantity of the product
    for i in lunch_ticket_orders:
        company_tickets += i.quantity

    unassigned_tickets = company_tickets - already_created_lunch_tickets.count()
    return unassigned_tickets, already_created_lunch_tickets


@require_GET
def lunchtickets_companysearch(request):
    """
    Search lunch tickets for the current fair & company
    """

    fair = Fair.objects.get(current=True)
    # ! TODO we're not checking if the company is actually who they say they are, this has to be fixed later
    # Check that auth-session matches a user that belongs to the company
    search_query = request.GET.get("company", "")
    if search_query == "":
        return JsonResponse({"message": "Company is empty."}, status=400)

    unassigned_tickets, lunch_tickets = company_total_lunch_tickets(fair, search_query)

    # Get Fair days
    days_result = FairDay.objects.filter(fair=fair).all()
    days = [day.date.strftime("%Y-%m-%d") for day in days_result]

    lunch_time_result = LunchTicketTime.objects.filter(day__in=days_result)

    lunch_times = [
        f'{time.day.date.strftime("%Y-%m-%d")} {time.name}'
        for time in lunch_time_result
    ]

    dietary_restrictions = DietaryRestriction.objects.all()
    dietary_restrictions_names = [
        restriction.name for restriction in dietary_restrictions
    ]

    data = {
        "assigned_lunch_tickets": [
            serializers.lunch_ticket_react(lunch_ticket)
            for lunch_ticket in lunch_tickets
        ],
        "unassigned_lunch_tickets": unassigned_tickets,
        # TODO fix time slots & rest of fields
        "fair_days": days,
        "lunch_times": lunch_times,
        "dietary_restrictions": dietary_restrictions_names,
    }

    return JsonResponse(data, safe=False)


def checkUserPermissionOnCompany(user, company):
    try:
        selectedCompanyID = (
            Company.objects.filter(name__exact=company).values("id").first()
        )
    except:
        return JsonResponse({"message": "Selected company is invalid."}, status=400)

    try:
        authCompanyID = (
            Company.objects.filter(name__exact=user.company).values("id").first()
        )
    except:
        return JsonResponse({"message": "Selected company is invalid."}, status=400)

    return authCompanyID == selectedCompanyID


@require_POST
def lunchticket_reactcreate(request):
    # Get authenticated's user company
    if not request.user.is_authenticated:
        return JsonResponse({"message": "User is not authenticated"}, status=403)

    user = get_object_or_404(CompanyContact, email_address=request.user)

    # Parse the JSON data from request.body
    data = json.loads(request.body)

    # TODO: Add authentication and check right privileges

    # Validate the data
    try:
        companyName = data.get("company")
    except:
        return JsonResponse({"message": "Company is empty."}, status=400)

    # Check user permission on this company

    if not checkUserPermissionOnCompany(user, companyName):
        return JsonResponse({"message": "Can't access this company data."}, status=403)

    try:
        date = data.get("day")
    except:
        return JsonResponse({"message": "Date is empty."}, status=400)

    try:
        lunch_time = data.get("time")
    except:
        return JsonResponse({"message": "Lunch time is empty."}, status=400)

    try:
        fair = Fair.objects.get(current=True)
    except:
        return JsonResponse(
            {"message": "Couldn't find current fair. Plase contact the staff"},
            status=500,
        )

    try:
        day = get_object_or_404(FairDay, date=date, fair=fair)
    except:
        return JsonResponse(
            {"message": "Couldn't find requested day. Plase contact the staff"},
            status=500,
        )

    date_part, time_part = str(lunch_time).split(" ")

    lunch_day = get_object_or_404(FairDay, date=date_part, fair=fair)
    time = get_object_or_404(LunchTicketTime, name=time_part, day=lunch_day)

    # Check that company can create more tickets
    try:
        (unassigned_tickets, _) = company_total_lunch_tickets(fair, companyName)
        if unassigned_tickets <= 0:
            return JsonResponse(
                {"Error": "Company has no more available tickets"}, status=400
            )
    except:
        return JsonResponse(
            {"message": "Could not load data from DB. Plase contact the staff"},
            status=500,
        )

    company = (
        Company.objects.filter(name__exact=data.get("company")).values("id").first()
    )

    if company is None:
        return JsonResponse(
            {
                "message": "Could not find your company in the database. Please contact the staff."
            },
            status=400,
        )
    company_id = company.get("id")

    # Begin a transaction
    with transaction.atomic():
        # Create the LunchTicket object
        lunch_ticket = LunchTicket(
            fair=fair,
            company_id=company_id,
            email_address=data.get("email_address"),
            comment=data.get("comment"),
            day_id=day.id,
            time_id=time.id,
            other_dietary_restrictions=data.get("other_dietary_restrictions"),
        )

        # Validate and save the object
        lunch_ticket.full_clean()  # This will raise ValidationError if any issues
        lunch_ticket.save()

        # Handle many-to-many field for dietary_restrictions
        dietary_restrictions_data = data.get("dietary_restrictions", {})

        # Fetch the DietaryRestriction objects that correspond to the selected items
        dietary_restrictions_objs = DietaryRestriction.objects.filter(
            name__in=dietary_restrictions_data
        )
        # Set the many-to-many relationship
        lunch_ticket.dietary_restrictions.set(dietary_restrictions_objs)

        lunch_ticket.save()  # Save the instance again to persist many-to-many changes

    return JsonResponse(
        {"token": lunch_ticket.token, "id": lunch_ticket.id}, status=200
    )


def lunchticket_reactremove(request, token):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "User is not authenticated"}, status=403)

    try:
        fair = Fair.objects.get(current=True)
    except:
        return JsonResponse(
            {"message": "Couldn't find current fair. Plase contact the staff"},
            status=500,
        )

    try:
        lunch_ticket = get_object_or_404(LunchTicket, fair=fair, token=token)
    except:
        return JsonResponse(
            {"message": "Couldn't find the selected ticket. Plase contact the staff"},
            status=500,
        )

    # Check if user has the right privileges over the lunch ticket company
    user = get_object_or_404(CompanyContact, email_address=request.user)
    if not checkUserPermissionOnCompany(user, lunch_ticket.company):
        return JsonResponse({"message": "Can't access this company data."}, status=403)

    try:
        lunch_ticket.delete()
    except:
        return JsonResponse(
            {"message": "Couldn't delete the selected ticket. Plase contact the staff"},
            status=500,
        )

    return HttpResponse(status=200)


def lunchticket_reactsend(request, token):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "User is not authenticated"}, status=403)

    try:
        fair = Fair.objects.get(current=True)
    except:
        return JsonResponse(
            {"message": "Couldn't find current fair. Plase contact the staff"},
            status=500,
        )

    try:
        lunch_ticket = get_object_or_404(LunchTicket, fair=fair, token=token)
    except:
        return JsonResponse(
            {"message": "Couldn't find the selected ticket. Plase contact the staff"},
            status=500,
        )

    # Check if user has the right privileges over the lunch ticket company
    user = get_object_or_404(CompanyContact, email_address=request.user)
    if not checkUserPermissionOnCompany(user, lunch_ticket.company):
        return JsonResponse({"message": "Can't access this company data."}, status=403)

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
        "Armada Lunch Ticket <noreply@armada.nu>",
        [email_address],
        fail_silently=True,
    )

    lunch_ticket.sent = True
    lunch_ticket.save()

    return HttpResponse(status=200)


@require_POST
@permission_required("fair.lunchtickets")
def lunchticket_check_in(request, lunch_ticket_pk):
    """
    Check in a lunch ticket
    """

    lunch_ticket = get_object_or_404(LunchTicket, pk=lunch_ticket_pk)

    lunch_ticket.used = True
    lunch_ticket.save()

    LunchTicketScan.objects.create(lunch_ticket=lunch_ticket, user=request.user)

    return HttpResponse(status=204)


@require_POST
@permission_required("fair.lunchtickets")
def lunchticket_check_out(request, lunch_ticket_pk):
    """
    Check out a lunch ticket
    """

    lunch_ticket = get_object_or_404(LunchTicket, pk=lunch_ticket_pk)

    lunch_ticket.used = False
    lunch_ticket.save()

    LunchTicketScan.objects.filter(lunch_ticket=lunch_ticket).delete()

    return HttpResponse(status=204)


@require_GET
@permission_required("fair.lunchtickets")
def lunchticket_check_in_by_token(request):
    """
    Get a lunch ticket by the check in token
    """

    token = request.GET.get("token")

    if token is None:
        return JsonResponse({"message": "No token in request."}, status=400)

    lunch_ticket = LunchTicket.objects.filter(token=token).first()

    if lunch_ticket is None:
        return JsonResponse(
            {"message": "Found no lunch ticket matching that code."}, status=404
        )

    if lunch_ticket.used is True:
        return JsonResponse(
            {"message": "Lunch ticket has already been used."}, status=403
        )

    lunch_ticket.used = True
    lunch_ticket.save()

    LunchTicketScan.objects.create(lunch_ticket=lunch_ticket, user=request.user)

    return JsonResponse({"lunch_ticket": serializers.lunch_ticket(lunch_ticket)})
