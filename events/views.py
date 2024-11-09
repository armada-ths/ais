import json

from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from events import serializers
from events.api import send_upgrade_email
from events.forms import EventForm, TeamForm
from events.models import Event, Team, Participant, SignupQuestion
from fair.models import Fair
from people.models import Programme
from recruitment.models import RecruitmentApplication


def save_questions(questions_data, event):
    questions = []
    questions_to_delete = list(SignupQuestion.objects.filter(event=event))

    for question in questions_data:
        pk = question.pop("id", None)

        defaults = {
            "event": event,
            "type": question["type"],
            "question": question["question"],
            "required": question["required"],
            "options": question["options"],
        }

        q, _created = SignupQuestion.objects.update_or_create(pk=pk, defaults=defaults)
        questions.append(q)

        if q in questions_to_delete:
            questions_to_delete.remove(q)

    for question in questions_to_delete:
        question.delete()


@permission_required("events.base")
def event_list(request, year):
    fair = get_object_or_404(Fair, year=year)
    events = Event.objects.annotate(
        num_participants=Count(
            "participant", filter=Q(participant__in_waiting_list=False)
        )
    ).filter(fair=fair)

    return render(request, "events/event_list.html", {"fair": fair, "events": events})


@permission_required("events.base")
def event_new(request, year):
    fair = get_object_or_404(Fair, year=year)

    react_props = {"question_types": dict(SignupQuestion.QUESTION_TYPES)}

    form = EventForm(request.POST or None, request.FILES or None)

    users = [
        recruitment_application.user
        for recruitment_application in RecruitmentApplication.objects.filter(
            status="accepted", recruitment_period__fair=fair
        ).order_by("user__first_name", "user__last_name")
    ]
    form.fields["contact_person"].choices = [("", "---------")] + [
        (user.pk, user.get_full_name())
        for user in users
        if user.has_perm("companies.base")
    ]

    if request.POST and form.is_valid():
        event = form.save()
        questions_data = json.loads(request.POST["questions"])

        save_questions(questions_data, event)
        return HttpResponse(status=200)

    return render(
        request,
        "events/event_new.html",
        {"fair": fair, "form": form, "react_props": react_props},
    )


@permission_required("events.base")
def event_edit(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    event = get_object_or_404(Event, pk=pk, fair=fair)

    participants = (
        Participant.objects_all.filter(event=event)
        .select_related("user_s__profile")
        .all()
    )
    print(Participant.waitlist_objects)
    signup_questions = event.signupquestion_set.all()

    react_props = {
        "questions": [
            serializers.signup_question(question) for question in signup_questions
        ],
        "question_types": dict(SignupQuestion.QUESTION_TYPES),
    }

    print(request.FILES)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)

    users = [
        recruitment_application.user
        for recruitment_application in RecruitmentApplication.objects.filter(
            status="accepted", recruitment_period__fair=event.fair
        ).order_by("user__first_name", "user__last_name")
    ]
    form.fields["contact_person"].choices = [("", "---------")] + [
        (user.pk, user.get_full_name())
        for user in users
        if user.has_perm("companies.base")
    ]

    if request.POST and form.is_valid():
        form.save()

        questions_data = json.loads(request.POST["questions"])

        save_questions(questions_data, event)
        return HttpResponse(status=204)

    return render(
        request,
        "events/event_edit.html",
        {
            "fair": fair,
            "event": event,
            "participants": participants,
            "questions": signup_questions,
            "form": form,
            "react_props": json.dumps(react_props),
        },
    )


@login_required
def event_signup(request, year, event_pk):
    event = get_object_or_404(Event, pk=event_pk)

    if not event.published:
        return render(request, "events/event_not_published.html", {"event": event})

    payment_url = reverse("events_api:payment", args=[event_pk])
    signup_url = reverse("events_api:signup", args=[event_pk])
    upload_url = reverse("events_api:upload", args=[event_pk])

    # Will be populated if user has completed signup before
    participant = Participant.objects_all.filter(
        user_s=request.user, event=event
    ).first()

    open_student_teams = Team.objects.filter(event=event, allow_join_s=True)

    react_props = {
        "event": serializers.event(event, request),
        "teams": [serializers.team(team) for team in open_student_teams],
        "payment_url": payment_url,
        "signup_url": signup_url,
        "upload_url": upload_url,
        "stripe_publishable": settings.STRIPE_PUBLISHABLE,
        "participant": serializers.participant(participant) if participant else None,
        "student_programs": [program.name for program in Programme.objects.all()],
    }

    return render(
        request,
        "events/event_signup.html",
        {
            "event": event,
            "participant": participant,
            "react_props": json.dumps(react_props, cls=DjangoJSONEncoder),
        },
    )


@permission_required("events.base")
def check_in(request, year, event_pk):
    event = get_object_or_404(Event, pk=event_pk)

    participants = Participant.objects.filter(event=event).all()

    react_props = {
        "participants": [
            serializers.participant(participant) for participant in participants
        ],
        "event_id": event_pk,
    }

    return render(
        request, "events/check_in.html", {"react_props": json.dumps(react_props)}
    )


@permission_required("events.base")
def team_edit(request, year, event_pk, team_pk):
    fair = get_object_or_404(Fair, year=year)
    event = get_object_or_404(Event, pk=event_pk)
    team = get_object_or_404(Team, pk=team_pk)

    form = TeamForm(request.POST or None, instance=team)

    if request.POST and form.is_valid():
        form.save()
        return redirect("events:event_edit", fair.year, event.id)

    return render(
        request, "events/team_edit.html", {"fair": fair, "team": team, "form": form}
    )


@permission_required("events.base")
def team_new(request, year, event_pk):
    fair = get_object_or_404(Fair, year=year)
    event = get_object_or_404(Event, pk=event_pk)

    form = TeamForm(
        request.POST or None, initial={"max_capacity": event.teams_default_max_capacity}
    )

    if request.POST and form.is_valid():
        # We want to add the event_id here before saving the team
        new_team = form.save(commit=False)
        new_team.event = event
        new_team.save()
        return redirect("events:event_edit", fair.year, event.id)

    return render(request, "events/team_edit.html", {"fair": fair, "form": form})


# def test_send_email(request, year, event_pk):
#    print("fore")
#    name = "lucia"
#    link = "hsdjn.se"
#    email = "cookie4lu@gmail.com"
#    send_upgrade_email(
#        request,
#        event_pk,
#        name,
#        link,
#        email,
#        template="events/waitlist_upgrade_email.html",
#        subject="Event Confirmation",
#    )
#    print("efter")
