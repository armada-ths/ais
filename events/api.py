import json

import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET

from events import serializers
from events.models import Event, Participant, SignupQuestion, SignupQuestionAnswer, Team, TeamMember, ParticipantCheckIn
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

    if not event.open_for_signup:
        return JsonResponse({'message': 'Event not open for sign ups.'}, status=403)

    participant, _created = Participant.objects.get_or_create(
        user_s=request.user,
        event=event
    )

    payment_intent = participant.stripe_charge_id
    payment_status = stripe.PaymentIntent.retrieve(payment_intent)['status']
    if payment_status == 'succeeded':
        participant.fee_payed_s = True

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
        return JsonResponse({'error': 'Authentication required.'}, status=403)

    participant, _created = Participant.objects.get_or_create(
        user_s=request.user,
        event=event
    )

    if participant.fee_payed_s:
        return JsonResponse({'error': 'Fee has already been paid.'}, status=400)

    # data = json.loads(request.body)

    # Stripe expects the amount in ören
    # token = data['token']

    stripe.api_version = '2019-09-09'

    stripe.api_key = settings.STRIPE_SECRET

	# session = None
    # # ---- New version of Stripe checkout
    # session = stripe.checkout.Session.create(
    #     payment_method_types=['card'],
	# 	locale='en',
    #     line_items=[{
    #         name: 'THS Armada Event',
    #         description: event.name,
    #         amount: event.fee_s * 100,
    #         currency: 'sek',
    #         quantity: 1,
    #     }],
    #     success_url='https://google.com',
    #     cancel_url='https://bing.com',
    # )
    intent = None

    if participant.stripe_charge_id == None:
        intent = stripe.PaymentIntent.create(
            amount = event.fee_s * 100, # Stripe wants the price in öre
            currency = 'sek',
            description = event.name,
            # receipt_email = invitation.email_address,
        )
        participant.stripe_charge_id = intent['id']
        participant.save()
    else: # retrieve existing payment intent
        # intent = stripe.PaymentIntent.retrieve(participant.stripe_charge_id)
        intent = stripe.PaymentIntent.create(
            amount = event.fee_s * 100, # Stripe wants the price in öre
            currency = 'sek',
            description = event.name,
            # receipt_email = invitation.email_address,
        )
        participant.stripe_charge_id = intent['id']
        participant.save()
    # # ----- End of new version

    # Old version of Stripe checkout
    # charge = stripe.Charge.create(
    #     amount=amount,
    #     currency='sek',
    #     description=event.name,
    #     source=token
    # )
    if intent:
        # participant.stripe_charge_id = session['id']
        # participant.fee_payed_s = True
        # participant.save()
        return JsonResponse({'client_secret': intent.client_secret}, status=200)
        # return HttpResponse(status=204)
    else:
        return JsonResponse({'error': 'Unable to create Stripe payment intent'}, status=503)

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

    TeamMember.objects.update_or_create(participant=participant, defaults={'team': team, 'leader': False})

    teams = Team.objects.filter(event=event).all()

    return JsonResponse({'teams': [serializers.team(team) for team in teams]}, status=201)


@require_POST
def leave_team(request, event_pk):
    """
    Endpoint to leave teams for the event
    """
    event = get_object_or_404(Event, pk=event_pk)

    if not request.user:
        return JsonResponse({'message': 'Authentication required.'}, status=403)

    Participant.objects.get(user_s=request.user, event=event).teammember_set.all().delete()

    teams = Team.objects.filter(event=event).all()

    return JsonResponse({'teams': [serializers.team(team) for team in teams]}, status=200)


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

    team = Team.objects.create(
        event=event,
        name=data['name'],
        max_capacity=event.teams_default_max_capacity,
    )

    TeamMember.objects.update_or_create(participant=participant, defaults={'team': team, 'leader': True})

    teams = Team.objects.filter(event=event).all()

    return JsonResponse({
        'teams': [serializers.team(team) for team in teams],
        'participant': serializers.participant(participant)
    }, status=200)


@require_POST
def update_team(request, event_pk, team_pk):
    """
    Endpoint to update a team
    """

    event = get_object_or_404(Event, pk=event_pk)
    team = get_object_or_404(Team, pk=team_pk)

    if not request.user:
        return JsonResponse({'message': 'Authentication required.'}, status=403)

    team_member = TeamMember.objects.filter(participant__user_s=request.user, team=team).first()

    if not team_member and team_member.leader:
        return JsonResponse({'message': 'Only the team leader can edit the team.'}, status=403)

    data = json.loads(request.body)

    if 'name' not in data or 'members' not in data:
        return JsonResponse({'message': 'Bad request.'}, status=400)

    Team.objects.filter(id=team_pk).update(name=data['name'])

    ids = [member['id'] for member in data['members']]

    team.teammember_set.exclude(id__in=ids).delete()

    teams = Team.objects.filter(event=event).all()
    participant = Participant.objects.get(user_s=request.user, event=event)

    return JsonResponse({
        'teams': [serializers.team(team) for team in teams],
        'participant': serializers.participant(participant)
    }, status=200)


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

    participant = Participant.objects.filter(event=event, check_in_token=check_in_token).first()

    if participant is None:
        return JsonResponse({'message': 'No participant with that check_in_token.'}, status=404)

    return JsonResponse({'participant': serializers.participant(participant)}, status=200)
