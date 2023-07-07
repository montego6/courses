from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from decouple import config
from .payment import fullfill_order

stripe.api_key = config('STRIPE_KEY')

endpoint_secret = config('STRIPE_WEBHOOK_SECRET')

# Create your views here.
def index(request):
    return HttpResponse('All is OK')


@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)
  
  if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
    session = stripe.checkout.Session.retrieve(
      event['data']['object']['id'],
      expand=['line_items'],
    )
    line_items = session.line_items
    # print(line_items)
    # print(session)
    # Fulfill the purchase...
    fullfill_order(line_items['data'][0]['price'], session['client_reference_id'])

  # Passed signature verification
  return HttpResponse(status=200)