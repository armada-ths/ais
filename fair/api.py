import operator
from functools import reduce
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from django.http import QueryDict
from fair import serializers
from fair.models import Fair, LunchTicket, LunchTicketScan, LunchTicketTime, FairDay
from companies.models import Company
from .forms import LunchTicketForm

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

@require_GET
def lunchtickets_companysearch(request):
    """
    Search lunch tickets for the current fair & company
    """

    fair = Fair.objects.get(current=True)
    search_query = request.GET.get("company", "")

    if search_query == "":
        return JsonResponse({"message": "Company is empty."}, status=400)

    lunch_tickets = LunchTicket.objects.filter(
        Q(fair=fair)
        & (
            Q(company__name__icontains=search_query)
        )
    ).all()

    data = {
        "result": [
            serializers.lunch_ticket(lunch_ticket) for lunch_ticket in lunch_tickets
        ]
    }

    return JsonResponse(data, safe=False)

@require_POST
@csrf_exempt
#This is an endpoint called by react
def lunchticket_reactcreate(request):

    #Preprocess data
    companyName = request.POST['company']
    year = request.POST['day'].split("-")[0]

    #Get company's ID value
    company = Company.objects.filter(name__exact=companyName).values('id').first()
    if company:
        company_id = company['id']
        print(company_id)
    else:
        return HttpResponse(status=400)
    
    #Build date time 
    fair = get_object_or_404(Fair, year=year)
    day = get_object_or_404(FairDay, date=request.POST['day'], fair=fair)
    time = get_object_or_404(LunchTicketTime, name=request.POST['time'], day=day)

    #Modify request to adapt to what DJango expects
    mutable_req = QueryDict('', mutable=True)
    mutable_req.update(request.POST)
    mutable_req['company'] = str(company_id)
    mutable_req['day'] = str(day.id)
    mutable_req['time'] = str(time.id)
    mutable_req['user'] = ''

    form = LunchTicketForm(mutable_req or None, initial={"fair": fair})
    if form.is_valid():
        form.instance.fair = fair
        lunch_ticket = form.save()
        return HttpResponse(status=200)

    return HttpResponse(status=400)

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
