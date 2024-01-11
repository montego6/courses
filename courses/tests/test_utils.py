from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
import pytest
from core import consts
import courses.tests.factories as ft

from courses.utils import ExtraContext, get_user_from_context, make_payment_context
from courses.models import CoursePayment


@pytest.mark.django_db
def test_get_user_from_context(user):
    request = RequestFactory()
    request.user = user
    context = {'request': request}
    assert get_user_from_context(context) == user


@pytest.mark.parametrize('anon_user', [True, False])
@pytest.mark.django_db
def test_get_user_from_context_none(anon_user):
    request = RequestFactory()
    if anon_user:
        request.user = AnonymousUser()
    context = {'request': request}
    assert get_user_from_context(context) is None


@pytest.mark.parametrize('payment_exists, result', [
    (False, consts.COURSE_OPTION_FREE),
    (True, consts.COURSE_OPTION_PREMIUM)
])
@pytest.mark.django_db
def test_make_payment_context(payment_exists, result, course, user):
    if payment_exists:
        CoursePayment.objects.create(
            course=course,
            student=user,
            option=consts.COURSE_OPTION_PREMIUM,
            status=consts.COURSE_PAYMENT_PAID,
            amount=1200
        )
    context = make_payment_context(course, user)
    assert context['payment'] == result


class TestExtraContext:
    
    @pytest.mark.django_db
    def test_is_author_true(self, user, disconnect_signals):
        course = ft.CourseFactory(author=user)
        extra_context = ExtraContext({}, user, course)
        assert extra_context.is_author()
    
    @pytest.mark.django_db
    def test_is_author_false(self, user, course):
        extra_context = ExtraContext({}, user, course)
        assert not extra_context.is_author()

    @pytest.mark.django_db
    def test_update_context(self, user, course):
        extra_context = ExtraContext({}, user, course)
        context = extra_context.update_context()
        expected_result = {
            'is_author': False,
            'user': user
        }
        assert context == expected_result



