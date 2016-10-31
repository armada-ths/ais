from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from events.forms import AttendenceForm
from events.models import EventQuestion, Event, EventAnswer, EventAttendence
from events.templatetags.event_extras import user_attending_event, \
    registration_open, user_eligible_event
from django.core.mail import send_mail
from django.utils import timezone


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
    if not user_eligible_event(request.user, event):
        raise Http404()
    questions = EventQuestion.objects.filter(event=pk).all()
    ea = EventAttendence.objects.filter(user=request.user, event=event).first()
    number_of_registrations = EventAttendence.objects.filter(event=event).count()
    questions_answers = [(question, EventAnswer.objects.filter(
        attendence=ea, question=question).first()) for question in questions]
    form = AttendenceForm(
        request.POST or None, questions_answers=questions_answers)
    if form.is_valid() and registration_open(event):
        if not ea:
            status = 'A'
            if event.attendence_approvement_required or (0 < event.capacity <= number_of_registrations):
                status = 'S'
            ea = EventAttendence.objects.create(
                user=request.user, event=event, status=status)
            if event.send_submission_mail:
                send_mail_on_submission(request.user, event)
        for (question, id, answer) in form.get_answers():
            EventAnswer.objects.update_or_create(
                question_id=id, attendence=ea, defaults={'answer': answer})
        return redirect('event_list')
    return render(request, template_name, {"event": event, "form": form})


def event_list(request, template_name='events/event_list.html'):
    events = Event.objects.filter(
        event_end__gt=timezone.now()).order_by('event_start')
    # Only show events that have a group in common with the user
    events = [e for e in events if user_eligible_event(request.user, e)]
    return render(request, template_name, {"events": events})


def event_unattend(request, pk):
    EventAttendence.objects.filter(
        event_id=pk, user_id=request.user.id).delete()
    return redirect('event_list')
