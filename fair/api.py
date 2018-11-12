import operator
from functools import reduce

from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from fair import serializers
from fair.models import Fair, LunchTicket, LunchTicketScan


@require_GET
def lunchtickets_search(request):
    """
    Search lunch tickets for the current fair
    """

    fair = Fair.objects.get(current=True)
    search_query = request.GET.get('query', '')

    if search_query == '':
        return JsonResponse({'message': 'Query is empty.'}, status=400)

    names = search_query.split()
    print(names)

    name_query = reduce(operator.__or__, [Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) for query in names])

    lunch_tickets = LunchTicket.objects.filter(
        Q(fair=fair) &
        Q(company__name__icontains=search_query) |
        Q(email_address__icontains=search_query) |
        name_query
    ).all()

    data = {
        'result': [serializers.lunch_ticket(lunch_ticket) for lunch_ticket in lunch_tickets]
    }

    return JsonResponse(data, safe=False)


@require_POST
@permission_required('fair.lunchtickets')
def lunchticket_check_in(request, lunch_ticket_pk):
    """
    Check in a lunch ticket
    """

    lunch_ticket = get_object_or_404(LunchTicket, pk=lunch_ticket_pk)

    lunch_ticket.used = True
    lunch_ticket.save()

    LunchTicketScan.objects.create(
        lunch_ticket=lunch_ticket,
        user=request.user
    )

    return HttpResponse(status=204)


@require_POST
@permission_required('fair.lunchtickets')
def lunchticket_check_out(request, lunch_ticket_pk):
    """
    Check out a lunch ticket
    """

    lunch_ticket = get_object_or_404(LunchTicket, pk=lunch_ticket_pk)

    lunch_ticket.used = False
    lunch_ticket.save()

    LunchTicketScan.objects.filter(lunch_ticket=lunch_ticket).delete()

    return HttpResponse(status=204)


@require_POST
@permission_required('fair.lunchtickets')
def lunchticket_get_by_token(request, token):
    """
    Get a lunch ticket by the check in token
    """

    lunch_ticket = LunchTicket.objects.filter(token=token).first()

    if lunch_ticket is None:
        return JsonResponse({'message': 'No lunch ticket with that token.'}, status=404)

    return JsonResponse({'lunch_ticket': serializers.lunch_ticket(lunch_ticket)})
