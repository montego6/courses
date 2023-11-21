from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import factory
from courses.models import Homework, TestCompletion
import factories as ft
import pytest

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def client_logged(user):
    client = APIClient()
    password = user.password
    user.set_password(user.password)
    user.save()
    client.login(username=user.username, password=password)
    yield client
    client.logout()


@pytest.mark.django_db
def test_create_test_completion(client_logged, test):
    data = factory.build(dict, FACTORY_CLASS=ft.TestCompletionFactory)
    data['test'] = test.id
    response = client_logged.post(reverse('test-completion'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert TestCompletion.objects.last() is not None


@pytest.mark.django_db
def test_create_homework(client, section):
    data = factory.build(dict, FACTORY_CLASS=ft.HomeworkFactory)
    data['section'] = section.id
    print(data)
    response = client.post(reverse('homework-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Homework.objects.last() is not None