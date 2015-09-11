from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from events.models import Event, EventAttendence

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'capacity','description']

def event_list(request, template_name='events/event_list.html'):
    events = Event.objects.all()
    data = {}
    data['object_list'] = events
    return render(request, template_name, data)

def event_create(request, template_name='events/event_form.html'):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, template_name, {'form':form})

def event_update(request, pk, template_name='events/event_form.html'):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, template_name, {'form':form})

def event_delete(request, pk, template_name='events/event_confirm_delete.html'):
    event = get_object_or_404(Event, pk=pk)
    if request.method=='POST':
        event.delete()
        return redirect('event_list')
    return render(request, template_name, {'object':event})

class EventAttendenceForm(ModelForm):
    class Meta:
        model = EventAttendence
        fields = ['name', 'mobile']

def event_create_attendence(request, template_name='events/event_form.html'):
    form = EventAttendenceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, template_name, {'form':form})
