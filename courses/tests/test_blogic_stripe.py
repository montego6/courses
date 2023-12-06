from django.test import RequestFactory
import pytest
import stripe
from courses import consts

from courses.blogic_stripe import StripeSession, create_stripe_upgrade_prices
from courses.models import StripeCourse

@pytest.fixture
def stripe_course(course):
    product = stripe.Product.create(name=course.name)
    option_prices = create_stripe_upgrade_prices(course, product)
    stripe_item = StripeCourse.objects.create(course=course, product=product['id'], option_prices=option_prices)
    yield stripe_item
    for option in option_prices.values():
        stripe.Price.modify(option['price'], active=False)
        if 'upgrade' in option:
            for upgrade in option['upgrade'].values():
                stripe.Price.modify(upgrade, active=False)
    for product in stripe.Product.list(limit=3)['data']:
        stripe.Product.modify(product['id'], active=False)


@pytest.fixture
def request_f(user):
    request = RequestFactory().get('/')
    request.user = user
    return request

class TestStripeSession:

    # def test_get_line_items(self):
    #     price = 'qwdfsdgv2131234lkxcz'
    #     expected_data = {
    #         'price': price,
    #         'quantity': 1
    #     }
    #     assert StripeSession.get_line_items(price) == expected_data

    @pytest.mark.django_db
    def test_create_session(self, stripe_course, request_f):
        stripe_session = StripeSession(stripe_course.course, consts.COURSE_OPTION_PREMIUM)
        line_items = stripe_session.get_line_items(stripe_course.option_prices[consts.COURSE_OPTION_PREMIUM]['price'])
        session = stripe_session.create_session(request_f, line_items, {})
        assert 'id' in session
        assert isinstance(session['id'], str)
        assert len(session['id']) > 0
        assert False

    # def test_1(self):
    #     print(stripe.Product.search(query=f"name~'Major realize gas air left close. Wall say big.'"))
    #     assert False