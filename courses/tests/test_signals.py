from unittest.mock import patch
import pytest
import courses.tests.factories as ft
from categories.tests.factories import CategoryFactory


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


