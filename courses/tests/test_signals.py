from unittest.mock import patch
import pytest
import courses.tests.factories as ft
from categories.tests.factories import CategoryFactory, SubjectFactory, SubCategoryFactory

@pytest.mark.parametrize('factory', [
    ft.AdditinalFileFactory,
    ft.TestFactory,
    ft.HomeworkFactory, 
    ft.LessonFactory
])
@pytest.mark.django_db
@patch('courses.signals.handlers.create_stripe_course_item')
def test_signal_create_section_item(mock_class, factory):
    with patch('courses.signals.handlers.create_section_item') as mock:
        model = factory()
        assert mock.called
        assert mock.call_count == 1


@pytest.mark.parametrize('factory', [
    ft.CourseFactory,
    CategoryFactory,
    SubCategoryFactory, 
    ft.UserFactory,
])
@pytest.mark.django_db
@patch('courses.signals.handlers.create_stripe_course_item')
def test_signal_create_section_item_fails(mock_class, factory):
    with patch('courses.signals.handlers.create_section_item') as mock:
        model = factory()
        assert not mock.called


@pytest.mark.django_db
def test_signal_create_stripe_course_item():
    with patch('courses.signals.handlers.create_stripe_course_item') as mock:
        model = ft.CourseFactory()
        assert mock.called
        assert mock.call_count == 1


@pytest.mark.django_db
def test_signal_create_stripe_course_item_fails():
    with patch('courses.signals.handlers.create_stripe_course_item') as mock:
        model = CategoryFactory()
        assert not mock.called


@pytest.mark.django_db
@patch('courses.signals.handlers.create_stripe_course_item')
def test_signal_calculate_video_length(mock_class):
    with patch('courses.signals.handlers.calculate_video_length') as mock:
        model = ft.LessonFactory()
        assert mock.called
        assert mock.call_count == 1


@pytest.mark.parametrize('factory', [
    ft.CourseFactory,
    ft.TestFactory,
    ft.AdditinalFileFactory, 
    ft.HomeworkFactory,
])
@pytest.mark.django_db
@patch('courses.signals.handlers.create_stripe_course_item')
def test_signal_create_section_item_fails(mock_class, factory):
    with patch('courses.signals.handlers.calculate_video_length') as mock:
        model = factory()
        assert not mock.called