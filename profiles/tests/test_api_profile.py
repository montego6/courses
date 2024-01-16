from django.urls import reverse
from rest_framework import status
import factory
from rest_framework.test import APIClient
from users.helpers import get_user_full_name
from profiles.models import TeacherProfile
from profiles.api.serializers import TeacherProfileSerializer
import profiles.tests.factories as ft
import pytest
from courses.tests.conftest import client, client_logged


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
def test_create_profile(client_logged):
    data = factory.build(dict, FACTORY_CLASS=ft.TeacherProfileFactory)
    response = client_logged.post(reverse('teacherprofile-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert TeacherProfile.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_update_profile(client, teacher_profile):
    data = factory.build(dict, FACTORY_CLASS=ft.TeacherProfileFactory)
    response = client.put(reverse('teacherprofile-detail', kwargs={'pk': teacher_profile.id}), data)
    
    expected_data = {
       'id': teacher_profile.id,
       'bio': data['bio'],
       'balance': teacher_profile.balance,
       'name': get_user_full_name(teacher_profile.user),
       'rating': 0,
       'students': 0,
       'courses': [],
    }

    teacher_profile.refresh_from_db()
    expected_data['avatar'] = response.wsgi_request.build_absolute_uri(teacher_profile.avatar.url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_partial_update_profile(client, teacher_profile):
    data = {
        'bio': 'test',
    }

    response = client.patch(reverse('teacherprofile-detail', kwargs={'pk': teacher_profile.id}), data)

    expected_data = {
       'id': teacher_profile.id,
       'bio': data['bio'],
       'balance': teacher_profile.balance,
       'name': get_user_full_name(teacher_profile.user),
       'rating': 0,
       'students': 0,
       'courses': [],
    }

    teacher_profile.refresh_from_db()
    expected_data['avatar'] = response.wsgi_request.build_absolute_uri(teacher_profile.avatar.url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_retrieve_profile(client, teacher_profile):
    response = client.get(reverse('teacherprofile-detail', kwargs={'pk': teacher_profile.id}))

    expected_data = TeacherProfileSerializer(teacher_profile, context={'request': response.wsgi_request}).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_lesson(client):
    profiles = ft.TeacherProfileFactory.create_batch(9)
    
    response = client.get(reverse('teacherprofile-list'))

    expected_data = TeacherProfileSerializer(profiles, many=True, context={'request': response.wsgi_request}).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_destroy_profile(client, teacher_profile):
    response = client.delete(reverse('teacherprofile-detail', kwargs={'pk': teacher_profile.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not TeacherProfile.objects.filter(id=teacher_profile.id).exists()


@pytest.mark.django_db
def test_has_user_profile_yes(client_with_user):
    client, user = client_with_user
    profile = ft.TeacherProfileFactory(user=user)
    response = client.get(reverse('has-teacher-profile'))

    expected_data = {
        'profile': True,
        'content': TeacherProfileSerializer(profile).data,
        'courses': []
    }

    assert expected_data == response.data

@pytest.mark.django_db
def test_has_user_profile_no(client_logged):
    response = client_logged.get(reverse('has-teacher-profile'))

    expected_data = {
        'profile': False,
    }

    assert expected_data == response.data