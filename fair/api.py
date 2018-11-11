from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from fair import serializers
from fair.models import Fair, LunchTicket


@require_GET
def lunchtickets_search(request):
    """
    Search lunch tickets for the current fair
    """

    fair = Fair.objects.get(current=True)
    search_query = request.GET.get('query', '')

    lunch_tickets = LunchTicket.objects.filter(
        Q(fair=fair) &
        Q(company__name__icontains=search_query) |
        Q(email_address__icontains=search_query) |
        Q(user__first_name__icontains=search_query) |
        Q(user__last_name__icontains=search_query)
    ).all()

    data = {
        'result': [serializers.lunch_ticket(lunch_ticket) for lunch_ticket in lunch_tickets]
    }

    return JsonResponse(data, safe=False)
