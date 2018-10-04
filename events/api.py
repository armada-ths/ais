import json

import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET

from events import serializers
from events.models import Event, Participant, SignupQuestion, SignupQuestionAnswer, Team, TeamMember
from fair.models import Fair


@require_GET
def index(request):
    """
    Returns all published events for this years fair
    """

    fair = Fair.objects.get(current=True)
    events = Event.objects.filter(fair=fair, published=True).prefetch_related('signupquestion_set')

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
def signup(request, event_pk):
    """
    Endpoint to signup to events
    """

    event = get_object_or_404(Event, pk=event_pk)
    if not request.user:
        return JsonResponse({'message': 'Authentication required.'}, status=403)

    participant, _created = Participant.objects.get_or_create(
        user_s=request.user,
        event=event
    )

    if event.fee_s > 0 and not participant.fee_payed_s:
        return JsonResponse({'message': 'Fee has not been payed'}, status=400)

    data = json.loads(request.body)
    answers = data['answers']

    questions = SignupQuestion.objects.filter(event=event).all()

    for question in questions:
        SignupQuestionAnswer.objects.update_or_create(
            participant=participant,
            signup_question=question,
            defaults={'answer': answers[str(question.pk)]})

    # TODO Check that all required questions have been answered

    participant.signup_complete = True
    participant.save()

    return JsonResponse({'participant': serializers.participant(participant)}, status=201)


@require_POST
def payment(request, event_pk):
    """
    Endpoint to process Stripe card tokens
    """

    event = get_object_or_404(Event, pk=event_pk)

    if not request.user:
        return JsonResponse({'message': 'Authentication required.'}, status=403)

    participant, _created = Participant.objects.get_or_create(
        user_s=request.user,
        event=event
    )

    if participant.fee_payed_s:
        return JsonResponse({'message': 'Fee has already been paid.'}, status=400)

    data = json.loads(request.body)

    # Stripe expects the amount in ören
    amount = event.fee_s * 100
    token = data['token']

    stripe.api_key = settings.STRIPE_SECRET
    charge = stripe.Charge.create(
        amount=amount,
        currency='sek',
        description=event.name,
        source=token
    )

    participant.stripe_charge_id = charge['id']
    participant.fee_payed_s = True
    participant.save()

    return HttpResponse(status=204)


@require_POST
def join_team(request, event_pk, team_pk):
    """
    Endpoint to join teams
    """
    event = get_object_or_404(Event, pk=event_pk)
    team = get_object_or_404(Team, pk=team_pk)

    if not request.user:
        return JsonResponse({'message': 'Authentication required.'}, status=403)

    if team.is_full():
        return JsonResponse({'message': 'Team is full.'}, status=400)

    participant = Participant.objects.get(user_s=request.user, event=event)

    if team.leader is None:
        # TODO Remove as leader if leader of another team
        TeamMember.objects.filter(participant=participant).delete()
        team.leader = request.user
        team.save()
    else:
        TeamMember.objects.update_or_create(participant=participant, defaults={'team': team})

    return JsonResponse({'team': serializers.team(team)}, status=201)


@require_POST
def create_team(request, event_pk):
    """
    Endpoint to create new teams for an event
    """

    event = get_object_or_404(Event, pk=event_pk)

    if not request.user:
        return JsonResponse({'message': 'Authentication required.'}, status=403)

    participant = Participant.objects.get(user_s=request.user, event=event)

    data = json.loads(request.body)

    # TODO
    #   Check if team name is take
    #   Check (and remove) if user is already member (or leader) of a team

    team = Team.objects.create(
        event=event,
        name=data['name'],
        leader=request.user,
        max_capacity=event.teams_default_max_capacity,
    )

    return JsonResponse({'team': serializers.team(team)}, status=200)
