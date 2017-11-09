from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.mail import send_mail, send_mass_mail
from django.utils import timezone
from django.forms import modelform_factory
from django.contrib.auth.decorators import permission_required

from recruitment.models import CustomFieldAnswer
from fair.models import Fair

from .forms import AttendenceForm, EventForm
from .models import EventQuestion, Event, EventAnswer, EventAttendence
from .templatetags.event_extras import user_attending_event, registration_open, user_eligible_event


def send_mail_on_submission(user, event):
    if user.email != "":
        send_mail(
            event.submission_mail_subject,
            event.submission_mail_body,
            'system@armada.nu',
            [user.email],
            fail_silently=False,
        )


def event_attend_form(request, year, pk, template_name='events/event_attend.html'):
    fair = get_object_or_404(Fair, year=year)
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
    print('Form is valid', form.is_valid())
    print('registration_open(event)', registration_open(event))
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
            print(question, id, answer)
            EventAnswer.objects.update_or_create(
                question_id=id, attendence=ea, defaults={'answer': answer})

        if not event.extra_field:
            # This creates an extra field
            event.save()
        event.extra_field.handle_answers_from_request(request, ea.user)
        return redirect('event_list', fair.year)

    return render(request, template_name, {
        "event": event, "form": form,
        "extra_field_questions_with_answers": event.extra_field.questions_with_answers_for_user(ea.user if ea else None) if event.extra_field else None,
        "fair": fair,
    })



def event_list(request, year, template_name='events/event_list.html'):
    fair = get_object_or_404(Fair, year=year)
    events = Event.objects.filter(fair=fair).order_by('-event_start')
    # Only show events that have a group in common with the user
    events = [e for e in events if user_eligible_event(request.user, e)]
    return render(request, template_name, {"events": events, "fair": fair})


def event_unattend(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    EventAttendence.objects.filter(
        event_id=pk, user_id=request.user.id).delete()
    return redirect('event_list', fair.year)


@permission_required('events.change_event', raise_exception=True)
def event_edit(request, year, pk=None, template_name='events/event_form.html'):
    fair = get_object_or_404(Fair, year=year)
    event = Event.objects.filter(pk=pk).first()
    form = EventForm(request.POST or None, request.FILES or None, instance=event)

    if form.is_valid():
        event = form.save(commit=False)
        event.fair = fair
        event.save()
        event.extra_field.handle_questions_from_request(request, 'extra_field')
        return redirect('event_list', fair.year)

    return render(request, template_name, {
        "event": event, "form": form,
        'custom_fields': event.extra_field.customfield_set.all() if event and event.extra_field else None,
        "fair": fair,
    })


@permission_required('events.change_event', raise_exception=True)
def event_attendants(request, year, pk, template_name='events/event_attendants.html'):
    fair = get_object_or_404(Fair, year=year)
    event = get_object_or_404(Event, pk=pk)

    if request.POST:
        attendance_pks = [int(pk) for pk in request.POST.getlist('selected')]
        for attendance in event.eventattendence_set.all():
            new_status = 'A' if attendance.pk in attendance_pks else 'D'
            if new_status != attendance.status:
                attendance.status = new_status
                attendance.save()

        approved_attendances = []
        declined_attendances = []
        for attendance in EventAttendence.objects.filter(status='A').filter(status='D'):
            if attendance.user & attendance.user.email & attendance.status=='A':
                approved_attendances.append(attendance.user.email)
            elif attendance.user & attendance.user.email & attendance.status=='D':
                declined_attendances.append(attendance.user.email)

        approved_message = (event.confirmation_mail_subject, event.confirmation_mail_body, 'system@armada.nu', approved_attendances)
        declined_message = (event.rejection_mail_subject, event.rejection_mail_body, 'system@armada.nu', declined_attendances)
        send_mass_mail((approved_message, declined_message), fail_silently=False)
        
    attendances_with_answers = []
    questions = event.eventquestion_set.all()
    extra_field_questions = event.extra_field.customfield_set.all() if event.extra_field else []

    for attendance in event.eventattendence_set.order_by('-submission_date').all():
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
        "fair": fair,
    })
