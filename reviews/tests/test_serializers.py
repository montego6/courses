from unittest.mock import Mock
import pytest
import factory
from users.helpers import get_user_full_name
from reviews.tests import factories as ft
from courses.tests.conftest import disconnect_signals, course, user
from reviews.api.serializers import ReviewSerializer, ReviewWithFullNameSerializer

@pytest.mark.django_db
def test_review_serializer(review, disconnect_signals):
    data = ReviewSerializer(review).data
    expected_data = {
       'id': review.id,
       'course': review.course.id,
       'student': review.student.id,
       'comment': review.comment,
       'rating': review.rating
    }
    
    assert data == expected_data


@pytest.mark.django_db
def test_review_serialize_data(course, user, disconnect_signals):
    data = factory.build(dict, FACTORY_CLASS=ft.ReviewFactory)
    data['student'] = user.id
    data['course'] = course.id
    serializer = ReviewSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


@pytest.mark.django_db
def test_review_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.ReviewFactory)
    serializer = ReviewSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}


@pytest.mark.django_db
def test_review_serialize_data_create(course, user, disconnect_signals):
    data = factory.build(dict, FACTORY_CLASS=ft.ReviewFactory)
    data['course'] = course.id
    request = Mock()
    request.user = user
    serializer = ReviewSerializer(data=data, context={'request': request})
    assert serializer.is_valid()
    assert serializer.errors == {}
    review = serializer.save()
    assert review.student == user


@pytest.mark.django_db
def test_review_full_name_serializer(review, disconnect_signals):
    data = ReviewWithFullNameSerializer(review).data
    expected_data = {
       'id': review.id,
       'course': review.course.id,
       'student': get_user_full_name(review.student),
       'comment': review.comment,
       'rating': review.rating
    }
    
    assert data == expected_data

