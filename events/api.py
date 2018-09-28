import json

import stripe
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET

from events import serializers
from events.models import Event, Participant, SignupQuestion, SignupQuestionAnswer
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

    return HttpResponse(status=200)


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

    stripe.api_key = "sk_test_l4sPsGIoc2f8sD5N4D2fZkBY"
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
