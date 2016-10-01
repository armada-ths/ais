from django.shortcuts import render, get_object_or_404, redirect
from events.forms import AttendenceForm
from events.models import EventQuestion, Event, EventAnswer, EventAttendence
from events.templatetags.event_extras import user_attending_event

def event_attend_form(request, pk, template_name='events/event_attend.html'):
    event = get_object_or_404(Event, pk=pk)
    event_questions = EventQuestion.objects.filter(event=pk).all()
    form = AttendenceForm(request.POST or None, questions=event_questions)
    if form.is_valid():
        if user_attending_event(request.user, event):
            # TODO update the attendence instead
            return render(request, template_name, {"event":event, "form":form})
        ea = EventAttendence.objects.create(user=request.user, event=event)
        ea.save()
        for (question, id, answer) in form.get_answers():
            EventAnswer.objects.create(question_id=id, attendence=ea, answer=answer)
        return render(request, template_name, {"event":event, "form":form})

    return render(request, template_name, {"event":event, "form":form})

def event_unattend(request, pk):
    EventAttendence.objects.filter(event_id=pk, user_id=request.user.id).delete()
    return redirect("/")
