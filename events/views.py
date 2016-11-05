from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from events.forms import AttendenceForm
from events.models import EventQuestion, Event, EventAnswer, EventAttendence
from events.templatetags.event_extras import user_attending_event, \
    registration_open, user_eligible_event
from django.core.mail import send_mail
from django.utils import timezone
from django.forms import modelform_factory
from django.contrib.auth.decorators import permission_required
from recruitment.models import CustomFieldAnswer


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

        if not event.extra_field:
            # This creates an extra field
            event.save()
        event.extra_field.handle_answers_from_request(request, ea.user)
        return redirect('event_list')

    return render(request, template_name, {
        "event": event, "form": form,
        "extra_field_questions_with_answers": event.extra_field.questions_with_answers_for_user(ea.user if ea else None) if event.extra_field else None
    })



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


@permission_required('events.change_event', raise_exception=True)
def event_edit(request, pk=None, template_name='events/event_form.html'):
    event = Event.objects.filter(pk=pk).first()
    EventForm = modelform_factory(Event, exclude=('extra_field', 'image'))
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        event = form.save()
        event.extra_field.handle_questions_from_request(request, 'extra_field')
        return redirect('event_list')

    return render(request, template_name, {
        "event": event, "form": form,
        'custom_fields': event.extra_field.customfield_set.all() if event and event.extra_field else None,
    })


@permission_required('events.change_event', raise_exception=True)
def event_attendants(request, pk, template_name='events/event_attendants.html'):
    event = get_object_or_404(Event, pk=pk)

    attendances_with_answers = []
    questions = event.eventquestion_set.all()
    extra_field_questions = event.extra_field.customfield_set.all() if event.extra_field else []

    for attendance in event.eventattendence_set.all():
        attendance_answers = []
        for question in questions:
            answer = EventAnswer.objects.filter(question=question, attendence=attendance).first()
            attendance_answers.append(answer)

        extra_field_answers = []
        if event.extra_field:
            for question in extra_field_questions:
                answer = CustomFieldAnswer.objects.filter(user=attendance.user, custom_field=question).first()
                extra_field_answers.append(answer)

        attendances_with_answers.append({
            'attendance': attendance,
            'answers': attendance_answers,
            'extra_field_answers': extra_field_answers
        })


    return render(request, template_name, {
        "event": event,
        "attendances_with_answers": attendances_with_answers,
        "questions": questions,
        "extra_field_questions": extra_field_questions,

    })