from django.urls import reverse
from rest_framework import status
import factory
from courses.models import Homework, TestCompletion
from courses.serializers import HomeworkSerializer
import factories as ft
import pytest



@pytest.mark.django_db
def test_create_test_completion(client_logged, test):
    data = factory.build(dict, FACTORY_CLASS=ft.TestCompletionFactory)
    data['test'] = test.id
    response = client_logged.post(reverse('test-completion'), data)
    assert response.status_code == status.HTTP_201_CREATED
    print(response.data)
    assert TestCompletion.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_create_homework(client, section):
    data = factory.build(dict, FACTORY_CLASS=ft.HomeworkFactory)
    data['section'] = section.id
    response = client.post(reverse('homework-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Homework.objects.last() is not None

@pytest.mark.django_db
def test_update_homework(client, section, homework):
    data = factory.build(dict, FACTORY_CLASS=ft.HomeworkFactory)
    data['section'] = section.id
    response = client.put(reverse('homework-detail', kwargs={'pk': homework.id}), data)
    
    expected_data = {
        'id': homework.id,
        'type': 'homework',
        'name': data['name'],
        'description': data['description'],
        'option': 'basic',
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data

@pytest.mark.django_db
def test_partial_update_homework(client, section, homework):
    data = {
        'name': 'test name',
        'section': section.id,
    }

    response = client.patch(reverse('homework-detail', kwargs={'pk': homework.id}), data)

    expected_data = {
        'id': homework.id,
        'name': data['name'],
        'description': homework.description,
        'option': 'basic',
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data
    homework.refresh_from_db()
    assert homework.section.id == data['section']


@pytest.mark.django_db
def test_retrieve_homework(client, homework):
    response = client.get(reverse('homework-detail', kwargs={'pk': homework.id}))

    expected_data = HomeworkSerializer(homework).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_homework(client, disconnect_signals):
    homeworks = ft.HomeworkFactory.create_batch(9)
    
    response = client.get(reverse('homework-list'))

    expected_data = HomeworkSerializer(homeworks, many=True).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_destroy_homework(client, homework):
    response = client.delete(reverse('homework-detail', kwargs={'pk': homework.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Homework.objects.filter(id=homework.id).exists()