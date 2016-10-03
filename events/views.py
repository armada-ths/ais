from django.shortcuts import render, get_object_or_404, redirect
from events.forms import AttendenceForm
from events.models import EventQuestion, Event, EventAnswer, EventAttendence
from events.templatetags.event_extras import user_attending_event
from django.core.mail import send_mail

def send_mail_on_submission(user, event):
    if user.email != "":
        send_mail(
            event.submission_mail_subject,
            event.submission_mail_body,
            'system@armada.nu',
            [user.email],
            fail_silently=False,
        )

def event_attend_form(request, pk, template_name='events/event_attend.html'):
    event = get_object_or_404(Event, pk=pk)
    questions = EventQuestion.objects.filter(event=pk).all()
    ea = EventAttendence.objects.filter(user=request.user, event=event).first()
    questions_answers = [(question, EventAnswer.objects.filter(attendence=ea, question=question).first()) for question in questions]
    form = AttendenceForm(request.POST or None, questions_answers=questions_answers)
    if form.is_valid():
        if not ea:
            ea = EventAttendence.objects.create(user=request.user, event=event)
            if event.send_submission_mail:
                send_mail_on_submission(request.user, event)
        for (question, id, answer) in form.get_answers():
            EventAnswer.objects.update_or_create(question_id=id, attendence=ea, defaults={'answer':answer})
        
        return redirect('event_list')

    return render(request, template_name, {"event":event, "form":form})

def event_list(request, template_name='events/event_list.html'):
    events = Event.objects.all().order_by('event_start')
    return render(request, template_name, {"events":events})

def event_unattend(request, pk):
    EventAttendence.objects.filter(event_id=pk, user_id=request.user.id).delete()
    return redirect('event_list')
