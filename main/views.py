from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import stripe
from decouple import config
from .payment import fullfill_order

stripe.api_key = config('STRIPE_KEY')

endpoint_secret = config('STRIPE_WEBHOOK_SECRET')


class IndexView(TemplateView):
  template_name = 'index.html'


class CourseCreateView(TemplateView):
  template_name = 'course-add.html'


class CoursePreviewView(TemplateView):
  template_name = 'course-preview.html'


class CourseContentView(TemplateView):
  template_name = 'course-content.html'


class CourseDetailView(TemplateView):
  template_name = 'course-single.html'


class CourseSearchView(TemplateView):
  template_name = 'search.html'


class CoursesBySubject(TemplateView):
  template_name = 'by_subject.html'


class CoursesBySubcategory(TemplateView):
  template_name = 'by_subcategory.html'

class CoursesByCategory(TemplateView):
  template_name = 'by_category.html'

class CourseEditView(TemplateView):
  template_name = 'course-edit.html'


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
    # Fulfill the purchase...
    fullfill_order(product_data=line_items['data'][0], client_id=session['client_reference_id'], metadata=session['metadata'])

  # Passed signature verification
  return HttpResponse(status=200)