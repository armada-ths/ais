from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required

from fair.models import Fair
from events.models import Event
from django.db.models import Count


@permission_required('events.base')
def list_events(request, year):
    fair = get_object_or_404(Fair, year=year)
    events = Event.objects.annotate(num_participants=Count('participant'))

    return render(request, 'events/list_events.html', {
        'fair': fair,
        'events': events
    })
