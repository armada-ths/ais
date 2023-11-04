import json
import operator
from functools import reduce

from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from banquet import serializers
from banquet.models import Banquet, Seat, Participant
from fair.models import Fair


@require_POST
@csrf_exempt
def save_seat(request, banquet_pk, seat_pk):
    banquet = get_object_or_404(Banquet, pk=banquet_pk)
    seat = get_object_or_404(Seat, table__banquet=banquet, pk=seat_pk)

    if not request.user:
        return JsonResponse({"message": "Authentication required."}, status=403)

    data = json.loads(request.body)

    seat.top = data["top"]
    seat.left = data["left"]
    seat.save()

    return JsonResponse({"status": "ok"}, status=200)


@require_GET
@permission_required("banquet.base")
def ticket_search(request):
    fair = Fair.objects.get(current=True)
    banquet = get_object_or_404(Banquet, fair=fair)
    search_query = request.GET.get("query", "")

    if search_query == "":
        return JsonResponse({"message": "Query is empty."}, status=400)

    names = search_query.split()

    name_query = reduce(
        operator.__or__,
        [
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__email=query)
            | Q(email_address__icontains=query)
            | Q(name__icontains=query)
            for query in names
        ],
    )

    company_name_query = Q(company__name__icontains=search_query)

    tickets = Participant.objects.filter(
        Q(banquet=banquet) & (company_name_query | name_query)
    ).all()

    data = {"result": [serializers.ticket(ticket) for ticket in tickets]}

    return JsonResponse(data, safe=False)


@require_POST
@permission_required("banquet.base")
def ticket_check_in(request, ticket_pk):
    participant = get_object_or_404(Participant, pk=ticket_pk)

    participant.ticket_scanned = True
    participant.save()

    return HttpResponse(status=204)


@require_POST
@permission_required("banquet.base")
def ticket_check_out(request, ticket_pk):
    participant = get_object_or_404(Participant, pk=ticket_pk)

    participant.ticket_scanned = False
    participant.save()

    return HttpResponse(status=204)


@require_GET
@permission_required("banquet.base")
def ticket_check_in_by_token(request):
    token = request.GET.get("token")

    if token is None:
        return JsonResponse({"message": "No token in request."}, status=400)

    participant = Participant.objects.filter(token=token).first()

    if participant is None:
        return JsonResponse(
            {"message": "Found no banquet ticket matching that code."}, status=404
        )

    if participant.ticket_scanned is True:
        return JsonResponse(
            {"message": "Banquet ticket has already been used."}, status=403
        )

    participant.ticket_scanned = True
    participant.save()

    return JsonResponse({"ticket": serializers.ticket(participant)})
