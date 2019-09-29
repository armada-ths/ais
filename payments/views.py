import json
import stripe
from django.conf import settings
from django.shortcuts import render, redirect

def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET
    stripe.api_version = '2019-09-09'
    intent = request.session['intent']
    client_secret = intent['client_secret']
    template_name = 'payments/checkout.html'

    return render(request, template_name, {
        'client_secret' : client_secret,
        'stripe_publishable': settings.STRIPE_PUBLISHABLE,
        'amount' : intent['amount']/100,
    })


def confirm(request):
	invitation_token = request.session['invitation_token']
	# print("Confirm function")
	# TODO: Check status on the paymentintent here.
	# Maybe set a boolean on the participant? Or we redirect to checkout if it has not succeeded and redirect to banquet only if it is okay.
	try:
		del request.session['intent']
	except KeyError:
		pass
	try:
		del request.session['invitation_token']
	except KeyError:
		pass
	return redirect('../banquet/' + invitation_token)

# below webhook might not have to be used
#def check_payment_status
#skicka med request och
'''def webhook():
  payload = request.get_data()
  sig_header = request.headers.get('STRIPE_SIGNATURE')
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # invalid payload
    return "Invalid payload", 400
  except stripe.error.SignatureVerificationError as e:
    # invalid signature
    return "Invalid signature", 400

  event_dict = event.to_dict()
  if event_dict['type'] == "payment_intent.succeeded":
    intent = event_dict['data']['object']
    print "Succeeded: ", intent['id']
    # Fulfill the customer's purchase
  elif event_dict['type'] == "payment_intent.payment_failed":
    intent = event_dict['data']['object']
    error_message = intent['last_payment_error']['message'] if intent.get('last_payment_error') else None
    print "Failed: ", intent['id'], error_message
    # Notify the customer that payment failed

  return "OK", 200'''
#kollar att status == suceeded hos payment intent objektet
#kolla accounting vyn där kallar vi på export order
#return render(request, 'url till banque.html',
#{
#})
