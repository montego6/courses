from django.test import RequestFactory
import pytest
import stripe
from courses import consts

from courses.blogic_stripe import StripePrice, StripeSession, create_stripe_course_item, create_stripe_upgrade_prices, delete_stripe_course_item
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


@pytest.fixture
def deactivate_product():
    yield
    for product in stripe.Product.list(limit=3)['data']:
        stripe.Product.modify(product['id'], active=False)

class TestStripeSession:

    def test_get_line_items(self):
        price = 'qwdfsdgv2131234lkxcz'
        expected_data = {
            'price': price,
            'quantity': 1
        }
        assert StripeSession.get_line_items(price) == expected_data

    @pytest.mark.stripe
    @pytest.mark.django_db
    def test_create_session(self, stripe_course, request_f):
        stripe_session = StripeSession(stripe_course.course, consts.COURSE_OPTION_PREMIUM)
        line_items = stripe_session.get_line_items(stripe_course.option_prices[consts.COURSE_OPTION_PREMIUM]['price'])
        session = stripe_session.create_session(request_f, line_items, {})
        assert 'id' in session
        assert isinstance(session['id'], str)
        assert len(session['id']) > 0

    
    @pytest.mark.stripe
    @pytest.mark.django_db
    def test_buy(self, stripe_course, request_f):
        stripe_session = StripeSession(stripe_course.course, consts.COURSE_OPTION_PREMIUM)
        session = stripe_session.buy(request_f)
        assert 'id' in session
        assert isinstance(session['id'], str)
        assert len(session['id']) > 0

    
    @pytest.mark.stripe
    @pytest.mark.django_db
    def test_upgrade(self, stripe_course, request_f):
        stripe_session = StripeSession(stripe_course.course, consts.COURSE_OPTION_PREMIUM, upgrade_from=consts.COURSE_OPTION_BASIC)
        session = stripe_session.upgrade(request_f)
        assert 'id' in session
        assert isinstance(session['id'], str)
        assert len(session['id']) > 0


class TestStripePrice:
    @pytest.mark.stripe
    def test_create(self):
        product = stripe.Product.create(name='test product')
        stripe_price = StripePrice(1200, product)
        price = stripe_price.create()
        assert 'id' in price
        assert isinstance(price['id'], str)
        assert len(price['id']) > 0
        stripe.Product.modify(product['id'], active=False)
        stripe.Price.modify(price['id'], active=False)


@pytest.mark.stripe
@pytest.mark.django_db
def test_create_stripe_upgrade_prices(course, deactivate_product):
    product = stripe.Product.create(name=course.name)
    option_prices = create_stripe_upgrade_prices(course, product)
    prev_options = []
    for idx, option_dict in enumerate(course.options):
        option = option_dict['option']
        assert option in option_prices
        assert isinstance(option_prices[option], dict)
        assert 'price' in option_prices[option]
        assert isinstance(option_prices[option]['price'], str)
        if idx > 0:
            assert 'upgrade' in option_prices[option]
            assert isinstance(option_prices[option]['upgrade'], dict)
            for prev_option in prev_options:
                assert prev_option in option_prices[option]['upgrade']
                assert isinstance(option_prices[option]['upgrade'][prev_option], str)
        prev_options.append(option)


@pytest.mark.stripe
@pytest.mark.django_db
def test_create_stripe_course_item(course, deactivate_product):
    create_stripe_course_item(course)
    assert StripeCourse.objects.filter(course=course).exists()


@pytest.mark.stripe
@pytest.mark.django_db
def test_delete_stripe_course_item(stripe_course):
    delete_stripe_course_item(stripe_course.course)
    assert not StripeCourse.objects.filter(course=stripe_course.course).exists()