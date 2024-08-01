import json
from django import forms

import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, login_required

from events import serializers
from events.forms import SignupQuestionAnswerFileForm
from events.models import (
    Event,
    Participant,
    SignupQuestion,
    SignupQuestionAnswer,
    SignupQuestionAnswerFile,
    Team,
    TeamMember,
    ParticipantCheckIn,
)
from fair.models import Fair
from people.models import Profile
from lib.KTH_Catalog import lookup_user_with_api, merge_user_info

from django.db.models import Count


@require_GET
def index(request):
    """
    Returns all published events for this year's fair
    """
    fair = Fair.objects.get(current=True)
    events = (
        Event.objects.filter(fair=fair, published=True)
        .prefetch_related("signupquestion_set")
        #.annotate(participant_count=Count("participant"))
    )

    data = [serializers.event(event, request) for event in events]

    return JsonResponse(data, safe=False)


@require_GET
def show(request, event_pk):
    """
    Returns a single published event
    """

    event = Event.objects.get(pk=event_pk)

    data = serializers.event(event, request)
    
    return JsonResponse(data, safe=False)


@require_POST
def upload_file(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    if not request.user:
        return JsonResponse({"error": "Authentication required."}, status=403)

    if not event.open_for_signup:
        return JsonResponse({"error": "Event not open for sign ups."}, status=403)

    form = SignupQuestionAnswerFileForm(request.POST, request.FILES)

    if not form.is_valid():
        error = form.errors.get_json_data(escape_html=True)

        return JsonResponse(
            {"error": "Unable to save file.", "reason": error}, status=400
        )

    form.save()

    return JsonResponse(
        {"file_pk": form.instance.pk},
        status=201,
    )


@require_POST
def signup(request, event_pk):
    """
    Endpoint to signup to events
    """

    event = get_object_or_404(Event, pk=event_pk)
    if not request.user:
        return JsonResponse({"error": "Authentication required."}, status=403)

    if not event.open_for_signup:
        return JsonResponse({"error": "Event not open for sign ups."}, status=403)

    if event.is_full():
        return JsonResponse({"message": "Event is fully booked."}, status=400)

    participant, _created = Participant.objects.get_or_create(
        user_s=request.user, event=event
    )

    data = json.loads(request.body)
    answers = data["answers"]
    participant.stripe_charge_id = data["intent_id"]

    # check if the user has paid successfully by checking the status of the Stripe payment intent
    if event.fee_s > 0:
        if participant.stripe_charge_id:
            try:
                payment_intent = stripe.PaymentIntent.retrieve(
                    participant.stripe_charge_id
                )
            except:
                payment_intent = None
                participant.fee_payed_s = False

            if payment_intent:
                if payment_intent["status"] == "succeeded":
                    participant.fee_payed_s = True
                else:
                    participant.fee_payed_s = False
        else:  # no stripe_charge_id
            participant.fee_payed_s = False

    if event.fee_s > 0 and not participant.fee_payed_s:
        return JsonResponse({"error": "Fee has not been payed."}, status=400)

    questions = SignupQuestion.objects.filter(event=event).all()

    for question in questions:
        file = None
        answer = answers[str(question.pk)]

        if question.type == "file_upload" and answer != None:
            try:
                file = SignupQuestionAnswerFile.objects.get(pk=answer)
            except:
                file = None

        SignupQuestionAnswer.objects.update_or_create(
            participant=participant,
            signup_question=question,
            file=file,
            defaults={"answer": answer},
        )

    # TODO Check that all required questions have been answered

    participant.signup_complete = True
    participant.save()

    return JsonResponse(
        {"participant": serializers.participant(participant)}, status=201
    )


@require_POST
def payment(request, event_pk):
    """
    Endpoint to process Stripe card tokens

        Payment Intents: https://stripe.com/docs/payments/payment-intents/web
        Stripe frontend in React: https://stripe.com/docs/recipes/elements-react#using-stripe-elements-in-react
    """

    event = get_object_or_404(Event, pk=event_pk)

    if not request.user:
        return JsonResponse({"error": "Authentication required."}, status=403)

    stripe.api_key = settings.STRIPE_SECRET
    intent = None

    # if participant.stripe_charge_id == None:
    intent = stripe.PaymentIntent.create(
        amount=event.fee_s * 100,  # Stripe wants the price in öre
        currency="sek",
        description=event.name,
    )
    if intent == None:
        return JsonResponse(
            {"error": "Unable to reach the external payment serivce provider."},
            status=503,
        )

    return JsonResponse(
        {"client_secret": intent.client_secret, "intent_id": intent.id}, status=200
    )


@require_POST
def join_team(request, event_pk, team_pk):
    """
    Endpoint to join teams
    """
    event = get_object_or_404(Event, pk=event_pk)
    team = get_object_or_404(Team, pk=team_pk)

    if not request.user:
        return JsonResponse({"message": "Authentication required."}, status=403)

    if team.is_full():
        return JsonResponse({"message": "Team is full."}, status=400)

    participant = Participant.objects.get(user_s=request.user, event=event)

    TeamMember.objects.update_or_create(
        participant=participant, defaults={"team": team, "leader": False}
    )

    teams = Team.objects.filter(event=event, allow_join_s=True).all()

    return JsonResponse(
        {"teams": [serializers.team(team) for team in teams]}, status=201
    )


@require_POST
def leave_team(request, event_pk):
    """
    Endpoint to leave teams for the event
    """
    event = get_object_or_404(Event, pk=event_pk)

    if not request.user:
        return JsonResponse({"message": "Authentication required."}, status=403)

    Participant.objects.get(
        user_s=request.user, event=event
    ).teammember_set.all().delete()

    teams = Team.objects.filter(event=event, allow_join_s=True).all()

    return JsonResponse(
        {"teams": [serializers.team(team) for team in teams]}, status=200
    )


@require_POST
def create_team(request, event_pk):
    """
    Endpoint to create new teams for an event
    """

    event = get_object_or_404(Event, pk=event_pk)

    if not request.user:
        return JsonResponse({"message": "Authentication required."}, status=403)

    participant = Participant.objects.get(user_s=request.user, event=event)

    data = json.loads(request.body)

    team = Team.objects.create(
        event=event,
        name=data["name"],
        max_capacity=event.teams_default_max_capacity,
    )

    TeamMember.objects.update_or_create(
        participant=participant, defaults={"team": team, "leader": True}
    )

    teams = Team.objects.filter(event=event, allow_join_s=True).all()

    return JsonResponse(
        {
            "teams": [serializers.team(team) for team in teams],
            "participant": serializers.participant(participant),
        },
        status=200,
    )


@require_POST
def update_team(request, event_pk, team_pk):
    """
    Endpoint to update a team
    """

    event = get_object_or_404(Event, pk=event_pk)
    team = get_object_or_404(Team, pk=team_pk)

    if not request.user:
        return JsonResponse({"message": "Authentication required."}, status=403)

    team_member = TeamMember.objects.filter(
        participant__user_s=request.user, team=team
    ).first()

    if not team_member and team_member.leader:
        return JsonResponse(
            {"message": "Only the team leader can edit the team."}, status=403
        )

    data = json.loads(request.body)

    if "name" not in data or "members" not in data:
        return JsonResponse({"message": "Bad request."}, status=400)

    Team.objects.filter(id=team_pk).update(name=data["name"])

    ids = [member["id"] for member in data["members"]]

    team.teammember_set.exclude(id__in=ids).delete()

    teams = Team.objects.filter(event=event, allow_join_s=True).all()
    participant = Participant.objects.get(user_s=request.user, event=event)

    return JsonResponse(
        {
            "teams": [serializers.team(team) for team in teams],
            "participant": serializers.participant(participant),
        },
        status=200,
    )


@require_POST
def check_in(request, event_pk, participant_pk):
    """
    Endpoint to check in a participant
    """
    get_object_or_404(Event, pk=event_pk)
    participant = get_object_or_404(Participant, pk=participant_pk)

    ParticipantCheckIn.objects.create(participant=participant)

    return HttpResponse(status=204)


@require_POST
def check_out(request, event_pk, participant_pk):
    """
    Endpoint to check out a participant
    """
    get_object_or_404(Event, pk=event_pk)
    participant = get_object_or_404(Participant, pk=participant_pk)

    ParticipantCheckIn.objects.filter(participant=participant).delete()

    return HttpResponse(status=204)


@require_POST
def get_by_token(request, event_pk, check_in_token):
    """
    Endpoint to get a participant by their check in token
    """
    event = get_object_or_404(Event, pk=event_pk)

    participant = Participant.objects.filter(
        event=event, check_in_token=check_in_token
    ).first()

    if participant is None:
        return JsonResponse(
            {"message": "No participant with that check_in_token."}, status=404
        )

    return JsonResponse(
        {"participant": serializers.participant(participant)}, status=200
    )


@require_GET
@permission_required("events.base")
@login_required
def fetch_participants_details(request, event_pk):
    """
    Endpoint to fetch participants details including email, first name and last name.
    """
    event = get_object_or_404(Event, pk=event_pk)

    participants = Participant.objects.filter(event=event)

    for participant in participants:
        user = participant.user_s
        if user is None:
            continue

        username = user.username
        details = lookup_user_with_api(username)

        if merge_user_info(user, details):
            user.save()

    return HttpResponse(status=200)
