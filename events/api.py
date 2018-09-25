from django.http import JsonResponse

from events import serializers
from events.models import Event
from fair.models import Fair


def index(request):
    '''
    Returns all published events for this years fair
    '''

    fair = Fair.objects.get(current=True)
    events = Event.objects.filter(fair=fair, published=True).prefetch_related('signupquestion_set')

    data = [serializers.event(event, request) for event in events]

    return JsonResponse(data, safe=False)


def show(request, pk):
    '''
    Returns a single published event
    '''

    event = Event.objects.get(pk=pk)

    data = serializers.event(event, request)

    return JsonResponse(data, safe=False)
