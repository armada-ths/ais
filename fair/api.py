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
from companies.models import Company
from people.models import DietaryRestriction
from .forms import LunchTicketForm
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy

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

    lunch_tickets = LunchTicket.objects.filter(
        fair=fair, company__name__exact=company_name
    ).all()

    # TODO Document this hardcoded query (relation to the category "Lunch Ticket")
    categories = Category.objects.filter(
        fair=fair, name__icontains="Lunch Ticket"  # Not case sensitive
    ).all()

    lunch_ticket_product = Product.objects.filter(
        category__in=categories
    ).all()  # Fetch all products that contain the category "[current_year]Lunch Ticket"

    company = Company.objects.filter(name__exact=company_name).values("id").first()
    # This list contains all the addition tickets that have been bought by the company this year
    additional_tickets_order = Order.objects.filter(
        product__in=lunch_ticket_product, purchasing_company__exact=company["id"]
    )

    # Find packages that contain tickets --> First: Find all ChildProducts related to LunchTickets[actual_year], Second: Find parent Products, Third: Find its correspondent orders for this company
    ticket_as_child_product = ChildProduct.objects.filter(
        child_product__in=lunch_ticket_product
    )
    products_containing_tickets = Product.objects.filter(
        child_products__in=ticket_as_child_product
    )
    orders_containing_tickets = Order.objects.filter(
        product__in=products_containing_tickets, purchasing_company__exact=company["id"]
    )

    # Let's count tickets
    company_tickets = 0

    # Now we got all the orders for this company that contain lunch tickets. Now let's count them going back to ChildProducts.quantity
    try:
        for order in orders_containing_tickets.select_related("product"):
            product_children_list = order.product.child_products.all()
            for child_product in product_children_list:
                if child_product in ticket_as_child_product:
                    company_tickets += child_product.quantity
    except:
        company_tickets = 0

    # Go through result and for each result get the quantity of the product
    for i in additional_tickets_order:
        company_tickets += i.quantity

    unassigned_tickets = company_tickets - lunch_tickets.count()
    return unassigned_tickets, lunch_tickets


@require_GET
def lunchtickets_companysearch(request):
    """
    Search lunch tickets for the current fair & company
    """

    fair = Fair.objects.get(current=True)
    # ! TODO we're not checking if the company is actually who they say they are, this has to be fixed later
    # Check that auth-session matches a user that belongs to the company
    search_query = request.GET.get("company", "")
    search_query = "3M"
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


@require_POST
@csrf_exempt
# This is an endpoint called by react
def lunchticket_reactcreate(request):
    # TODO: Add authentication and check right privileges

    # Preprocess data
    try:
        companyName = request.POST["company"]
    except:
        return JsonResponse({"message": "Company is empty."}, status=400)

    try:
        date = request.POST["day"]
    except:
        return JsonResponse({"message": "Date is empty."}, status=400)

    try:
        lunch_time = request.POST["time"]
    except:
        return JsonResponse({"message": "Lunch time is empty."}, status=400)

    # Extract request variables
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

    try:
        time = get_object_or_404(LunchTicketTime, name=lunch_time, day=day)
    except:
        return JsonResponse(
            {"message": "Couldn't find requested lunch time. Plase contact the staff"},
            status=500,
        )

    try:
        (unassigned_tickets, _) = company_total_lunch_tickets(fair, companyName)
    except:
        return JsonResponse(
            {"message": "Could not load data from DB. Plase contact the staff"},
            status=500,
        )

    if unassigned_tickets <= 0:
        return JsonResponse(
            {"Error": "Company has no more available tickets"}, status=400
        )

    # Get company's ID value

    company = Company.objects.filter(name__exact=companyName).values("id").first()
    if company:
        company_id = company["id"]
    else:
        return JsonResponse(
            {
                "message": "Could not find your company in the database. Please contact the staff."
            },
            status=400,
        )

    # Modify request to adapt to what DJango expects
    mutable_req = QueryDict("", mutable=True)
    mutable_req.update(request.POST)
    mutable_req["company"] = str(company_id)
    mutable_req["day"] = str(day.id)
    mutable_req["time"] = str(time.id)
    mutable_req["user"] = ""

    form = LunchTicketForm(mutable_req or None, initial={"fair": fair})
    if form.is_valid_react():
        form.instance.fair = fair
        lunch_ticket = form.save()
        return HttpResponse(status=200)

    return JsonResponse({"Error": "Could not create a ticket"}, status=400)


def lunchticket_reactremove(request, token):
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

    try:
        lunch_ticket.delete()
    except:
        return JsonResponse(
            {"message": "Couldn't delete the selected ticket. Plase contact the staff"},
            status=500,
        )

    return HttpResponse(status=200)


def lunchticket_reactsend(request, token):
    fair = Fair.objects.get(current=True)
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
