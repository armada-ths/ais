import json
import stripe
import time
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from banquet.models import Participant, Invitation

def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET
    # stripe.api_version = '2019-09-09'

    try:
        intent = request.session['intent']
    except KeyError:
        raise Http404

    client_secret = intent['client_secret']
    template_name = 'payments/checkout.html'

    return render(request, template_name, {
        'client_secret' : client_secret,
        'stripe_publishable': settings.STRIPE_PUBLISHABLE,
        'amount' : intent['amount']/100,
    })


def confirm(request):
    try:
        invitation_token = request.session['invitation_token']
    except KeyError:
        raise Http404

    try:
        intent = request.session['intent']
    except KeyError:
        raise Http404

    try:
        url_path = request.session['url_path']
    except KeyError:
        raise Http404

    invitation = get_object_or_404(Invitation, token=invitation_token)
    id = intent['id']

    test_status = 0
    while stripe.PaymentIntent.retrieve(id)['status'] != 'succeeded' and test_status != 5:
        time.sleep(3)
        test_status += 1

    if stripe.PaymentIntent.retrieve(id)['status'] != 'succeeded':
        invitation.participant.has_paid = False
        invitation.participant.save()
        # if we are unable to get status succeeded we send an email to support, the issue then has to be handled manually
        send_mail(
            'Problem with a payment in Stripe',
            'There have been a problem with the charge for the token ' + invitation_token + ' and the intent id ' + id,
            'noreply@armada.nu',
            ['support@armada.nu'],
            fail_silently=False,
        )

    else:
        invitation.participant.has_paid = True
        invitation.participant.save()

    try:
        del request.session['intent']
    except KeyError:
        pass
        
    try:
        del request.session['invitation_token']
    except KeyError:
        pass

    try:
        del request.session['url_path']
    except KeyError:
        pass

    return redirect(url_path)
    #return redirect('../banquet/' + invitation_token)
