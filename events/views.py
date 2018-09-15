from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

from fair.models import Fair
from events.models import Event
from django.db.models import Count
from events.forms import EventForm


@permission_required('events.base')
def list_events(request, year):
    fair = get_object_or_404(Fair, year=year)
    events = Event.objects.annotate(num_participants=Count('participant'))

    return render(request, 'events/list_events.html', {
        'fair': fair,
        'events': events
    })


@permission_required('events.base')
def event_new(request, year):
    fair = get_object_or_404(Fair, year=year)

    form = EventForm(request.POST or None)

    if request.POST and form.is_valid():
        form.save()
        return redirect('list_events', fair.year)

    return render(request, 'events/new_event.html', {
        'fair': fair,
        'form': form
    })
