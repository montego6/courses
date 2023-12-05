from unittest.mock import Mock
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
import pytest
from courses import consts
import factories as ft

from courses.blogic import ExtraContext, calculate_video_length, get_test_completion_result, get_user_from_context, has_user_full_access, make_payment_context
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


@pytest.mark.django_db
def test_get_test_completion_result(user, test):
    context = {
        'user': user
    }
    test_completion = ft.TestCompletionFactory(student=user, test=test)
    result = get_test_completion_result(context, test)
    assert result == test_completion.result


@pytest.mark.django_db
def test_get_test_completion_result_false(user, test):
    context = {
        'user': user
    }
    result = get_test_completion_result(context, test)
    assert result is False


@pytest.mark.parametrize('model', [
    ft.LessonFactory,
    ft.AdditinalFileFactory,
    ft.TestFactory,
    ft.HomeworkFactory
])
@pytest.mark.django_db
def test_has_user_full_access_author(model, disconnect_signals):
    context = {
        'is_author': True
    }
    instance = model()
    assert has_user_full_access(context, instance)


@pytest.mark.parametrize('model', [
    ft.LessonFactory,
    ft.AdditinalFileFactory,
    ft.TestFactory,
    ft.HomeworkFactory
])
@pytest.mark.django_db
def test_has_user_full_access_paid(model, disconnect_signals):
    context = {
        'payment': consts.COURSE_OPTION_PREMIUM
    }
    instance = model(option=consts.COURSE_OPTION_EXTRA)
    assert has_user_full_access(context, instance)


@pytest.mark.parametrize('model', [
    ft.LessonFactory,
    ft.AdditinalFileFactory,
    ft.TestFactory,
    ft.HomeworkFactory
])
@pytest.mark.django_db
def test_has_user_full_access_not_paid(model, disconnect_signals):
    context = {
        'payment': consts.COURSE_OPTION_BASIC
    }
    instance = model(option=consts.COURSE_OPTION_EXTRA)
    assert not has_user_full_access(context, instance)


@pytest.mark.parametrize('model', [
    ft.LessonFactory,
    ft.AdditinalFileFactory,
    ft.TestFactory,
    ft.HomeworkFactory
])
@pytest.mark.django_db
def test_has_user_full_access_not_paid_author(model, disconnect_signals):
    context = {
        'is_author': True,
        'payment': consts.COURSE_OPTION_BASIC
    }
    instance = model(option=consts.COURSE_OPTION_EXTRA)
    assert has_user_full_access(context, instance)


@pytest.mark.django_db
def test_calculate_video_length(lesson):
    assert lesson.duration is None
    calculate_video_length(lesson)
    lesson.refresh_from_db()
    assert lesson.duration == 63