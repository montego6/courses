from django.urls import reverse
from rest_framework import status
import factory
from ..models import Test, TestCompletion
from sectionitems.api.serializers import TestSerializer
import sectionitems.tests.factories as ft
import pytest


@pytest.mark.django_db
def test_create_test_completion(client_logged, test):
    data = factory.build(dict, FACTORY_CLASS=ft.TestCompletionFactory)
    data['test'] = test.id
    response = client_logged.post(reverse('api:test-completion'), data)
    assert response.status_code == status.HTTP_201_CREATED
    print(response.data)
    assert TestCompletion.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_create_test(client, section):
    data = factory.build(dict, FACTORY_CLASS=ft.TestFactory)
    data['section'] = section.id
    response = client.post(reverse('api:test-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Test.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_update_test(client, section, test):
    data = factory.build(dict, FACTORY_CLASS=ft.TestFactory)
    data['section'] = section.id
    response = client.put(reverse('api:test-detail', kwargs={'pk': test.id}), data)
    
    expected_data = {
        'id': test.id,
        'type': 'test',
        'name': data['name'],
        'description': data['description'],
        'option': 'basic',
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_partial_update_test(client, section, test):
    data = {
        'name': 'test name',
        'section': section.id,
    }

    response = client.patch(reverse('api:test-detail', kwargs={'pk': test.id}), data)

    expected_data = {
        'id': test.id,
        'name': data['name'],
        'description': test.description,
        'option': 'basic',
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data
    test.refresh_from_db()
    assert test.section.id == data['section']


@pytest.mark.django_db
def test_retrieve_test(client, test):
    response = client.get(reverse('api:test-detail', kwargs={'pk': test.id}))

    expected_data = TestSerializer(test).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_test(client, disconnect_signals):
    tests = ft.TestFactory.create_batch(9)
    response = client.get(reverse('api:test-list'))
    expected_data = TestSerializer(tests, many=True).data
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_destroy_test(client, test):
    response = client.delete(reverse('api:test-detail', kwargs={'pk': test.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Test.objects.filter(id=test.id).exists()