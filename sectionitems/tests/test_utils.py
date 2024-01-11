from django.contrib.admin.options import get_content_type_for_model
import pytest
from sectionitems.models import SectionItem
import sectionitems.tests.factories as ft
from sectionitems.utils import calculate_video_length, create_section_item, get_test_completion_result, has_user_full_access
from core import consts

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


@pytest.mark.parametrize('model', [
    ft.LessonFactory,
    ft.AdditinalFileFactory,
    ft.TestFactory,
    ft.HomeworkFactory
])
@pytest.mark.django_db
def test_create_section_item(model, disconnect_signals):
    instance = model()
    create_section_item(instance)
    assert SectionItem.objects.filter(content_type=get_content_type_for_model(instance), object_id=instance.id, section=instance.section)