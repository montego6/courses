from django.test import RequestFactory
import pytest
import stripe
from core import consts

from courses.blogic_stripe import StripePrice, StripeSession, create_stripe_course_item, create_stripe_upgrade_prices, delete_stripe_course_item
from courses.models import CoursePrice, CourseUpgradePrice, StripeCourse


@pytest.fixture
def stripe_course(course):
    product = stripe.Product.create(name=course.name)
    CoursePrice.objects.create(course=course, option=consts.COURSE_OPTION_BASIC, amount=1000)
    CoursePrice.objects.create(course=course, option=consts.COURSE_OPTION_EXTRA, amount=2000)
    CoursePrice.objects.create(course=course, option=consts.COURSE_OPTION_PREMIUM, amount=2500)
    stripe_item = StripeCourse.objects.create(course=course, product=product['id'])
    create_stripe_upgrade_prices(course)
    yield stripe_item
    for product in stripe.Product.list(limit=4)['data']:
        stripe.Product.modify(product['id'], active=False)


@pytest.fixture
def request_f(user):
    request = RequestFactory().get('/')
    request.user = user
    return request


@pytest.fixture
def deactivate_product():
    yield
    for product in stripe.Product.list(limit=4)['data']:
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
        price = CoursePrice.objects.get(course=stripe_course.course, option=consts.COURSE_OPTION_PREMIUM)
        line_items = stripe_session.get_line_items(price.stripe)
        session = stripe_session.create_session(request_f, line_items, {})
        assert 'id' in session
        assert isinstance(session['id'], str)
        assert len(session['id']) > 0

    
    @pytest.mark.stripe
    @pytest.mark.django_db
    def test_buy(self, stripe_course, request_f):
        stripe_session = StripeSession(stripe_course.course, consts.COURSE_OPTION_PREMIUM)
        price = CoursePrice.objects.get(course=stripe_course.course, option=consts.COURSE_OPTION_PREMIUM)
        session = stripe_session.buy(request_f, price)
        assert 'id' in session
        assert isinstance(session['id'], str)
        assert len(session['id']) > 0

    
    @pytest.mark.stripe
    @pytest.mark.django_db
    def test_upgrade(self, stripe_course, request_f):
        stripe_session = StripeSession(stripe_course.course, consts.COURSE_OPTION_PREMIUM, upgrade_from=consts.COURSE_OPTION_BASIC)
        for obj in CourseUpgradePrice.objects.all():
            print(obj)
        upgrade_price = CourseUpgradePrice.objects.get(course=stripe_course.course, from_option=consts.COURSE_OPTION_BASIC, 
                                                       to_option=consts.COURSE_OPTION_PREMIUM)
        
        session = stripe_session.upgrade(request_f, upgrade_price)
        assert 'id' in session
        assert isinstance(session['id'], str)
        assert len(session['id']) > 0


class TestStripePrice:
    @pytest.mark.stripe
    def test_create(self):
        product = stripe.Product.create(name='test product')
        stripe_price = StripePrice(1200, product['id'])
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
    StripeCourse.objects.create(course=course, product=product['id'])
    CoursePrice.objects.create(course=course, option=consts.COURSE_OPTION_BASIC, amount=1000)
    CoursePrice.objects.create(course=course, option=consts.COURSE_OPTION_EXTRA, amount=2000)
    CoursePrice.objects.create(course=course, option=consts.COURSE_OPTION_PREMIUM, amount=2500)
    create_stripe_upgrade_prices(course)
    assert CoursePrice.objects.count() == 3
    assert CourseUpgradePrice.objects.count() == 3
    for price in CoursePrice.objects.all():
        assert price.stripe
    for upgrade_price in CourseUpgradePrice.objects.all():
        assert upgrade_price.stripe
    


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