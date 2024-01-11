from unittest.mock import patch
import pytest
from categories.tests.factories import CategoryFactory, SubCategoryFactory
from courses.tests.factories import CourseFactory, UserFactory
import sectionitems.tests.factories as ft

@pytest.mark.parametrize('factory', [
    ft.AdditinalFileFactory,
    ft.TestFactory,
    ft.HomeworkFactory, 
    ft.LessonFactory
])
@pytest.mark.django_db
@patch('courses.signals.handlers.create_stripe_course_item')
def test_signal_create_section_item(mock_class, factory):
    with patch('sectionitems.signals.handlers.create_section_item') as mock:
        model = factory()
        assert mock.called
        assert mock.call_count == 1


@pytest.mark.parametrize('factory', [
    CourseFactory,
    CategoryFactory,
    SubCategoryFactory, 
    UserFactory,
])
@pytest.mark.django_db
@patch('courses.signals.handlers.create_stripe_course_item')
def test_signal_create_section_item_fails(mock_class, factory):
    with patch('sectionitems.signals.handlers.create_section_item') as mock:
        model = factory()
        assert not mock.called


@pytest.mark.django_db
@patch('courses.signals.handlers.create_stripe_course_item')
def test_signal_calculate_video_length(mock_class):
    with patch('sectionitems.signals.handlers.calculate_video_length') as mock:
        model = ft.LessonFactory()
        assert mock.called
        assert mock.call_count == 1


@pytest.mark.parametrize('factory', [
    CourseFactory,
    ft.TestFactory,
    ft.AdditinalFileFactory, 
    ft.HomeworkFactory,
])
@pytest.mark.django_db
@patch('courses.signals.handlers.create_stripe_course_item')
def test_signal_calculate_video_length_fails(mock_class, factory):
    with patch('sectionitems.signals.handlers.calculate_video_length') as mock:
        model = factory()
        assert not mock.called