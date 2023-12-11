from django.urls import reverse
from rest_framework import status
import factory
from courses.models import Lesson
from courses.serializers import LessonSerializer
import courses.tests.factories as ft
import pytest



@pytest.mark.django_db
def test_create_lesson(client, section):
    data = factory.build(dict, FACTORY_CLASS=ft.LessonFactory)
    data['section'] = section.id
    response = client.post(reverse('lesson-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Lesson.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_update_lesson(client, section, lesson):
    data = factory.build(dict, FACTORY_CLASS=ft.LessonFactory)
    data['section'] = section.id
    response = client.put(reverse('lesson-detail', kwargs={'pk': lesson.id}), data)
    
    expected_data = {
        'id': lesson.id,
        'type': 'lesson',
        'name': data['name'],
        'description': data['description'],
        'option': 'basic',
        'duration': None,
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_partial_update_lesson(client, section, lesson):
    data = {
        'name': 'test name',
        'section': section.id,
    }

    response = client.patch(reverse('lesson-detail', kwargs={'pk': lesson.id}), data)

    expected_data = {
        'id': lesson.id,
        'name': data['name'],
        'description': lesson.description,
        'option': 'basic',
        'duration': None,
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data
    lesson.refresh_from_db()
    assert lesson.section.id == data['section']


@pytest.mark.django_db
def test_retrieve_lesson(client, lesson):
    response = client.get(reverse('lesson-detail', kwargs={'pk': lesson.id}))

    expected_data = LessonSerializer(lesson).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_lesson(client, disconnect_signals):
    lessons = ft.LessonFactory.create_batch(9)
    
    response = client.get(reverse('lesson-list'))

    expected_data = LessonSerializer(lessons, many=True).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_destroy_lesson(client, lesson):
    response = client.delete(reverse('lesson-detail', kwargs={'pk': lesson.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Lesson.objects.filter(id=lesson.id).exists()