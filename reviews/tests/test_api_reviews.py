from django.urls import reverse
from rest_framework import status
import factory
from rest_framework.test import APIClient
from profiles.models import TeacherProfile
from profiles.api.serializers import TeacherProfileSerializer
from reviews.models import Review
from reviews.api.serializers import ReviewSerializer
import reviews.tests.factories as ft
import pytest
from courses.tests.conftest import client, client_logged, course, user, disconnect_signals


@pytest.fixture
def client_with_user(user):
    client = APIClient()
    password = user.password
    user.set_password(user.password)
    user.save()
    client.login(username=user.username, password=password)
    yield client, user
    client.logout()


@pytest.mark.django_db
def test_create_review(client_with_user, course, disconnect_signals):
    client, user = client_with_user
    data = factory.build(dict, FACTORY_CLASS=ft.ReviewFactory)
    data['course'] = course.id
    response = client.post(reverse('review-create'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.filter(id=response.data['id']).exists()
    assert Review.objects.get(id=response.data['id']).student == user


@pytest.mark.django_db
def test_list_reviews(client, course):
    reviews = ft.ReviewFactory.create_batch(9, course=course)
    response = client.get(reverse('review-list', kwargs={'pk': course.id}))
    expected_data = ReviewSerializer(reviews, many=True).data
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


