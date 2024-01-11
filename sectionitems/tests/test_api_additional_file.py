from django.urls import reverse
from rest_framework import status
import factory
from courses.models import AdditionalFile
from courses.api.serializers import AdditionalFileSerializer
import courses.tests.factories as ft
import pytest



@pytest.mark.django_db
def test_create_additional_file(client, section, delete_test_files):
    data = factory.build(dict, FACTORY_CLASS=ft.AdditinalFileFactory)
    data['section'] = section.id
    response = client.post(reverse('additionalfile-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert AdditionalFile.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_update_additional_file(client, section, additional_file, delete_test_files):
    data = factory.build(dict, FACTORY_CLASS=ft.AdditinalFileFactory)
    data['section'] = section.id
    response = client.put(reverse('additionalfile-detail', kwargs={'pk': additional_file.id}), data)
    
    expected_data = {
        'id': additional_file.id,
        'type': 'extra_file',
        'name': data['name'],
        'description': data['description'],
        'option': 'basic',
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_partial_update_additional_file(client, section, additional_file):
    data = {
        'name': 'test name',
        'section': section.id,
    }

    response = client.patch(reverse('additionalfile-detail', kwargs={'pk': additional_file.id}), data)

    expected_data = {
        'id': additional_file.id,
        'name': data['name'],
        'description': additional_file.description,
        'option': 'basic',
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data
    additional_file.refresh_from_db()
    assert additional_file.section.id == data['section']


@pytest.mark.django_db
def test_retrieve_additional_file(client, additional_file):
    response = client.get(reverse('additionalfile-detail', kwargs={'pk': additional_file.id}))

    expected_data = AdditionalFileSerializer(additional_file).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_additional_file(client, disconnect_signals):
    additional_files = ft.AdditinalFileFactory.create_batch(9)
    
    response = client.get(reverse('additionalfile-list'))

    expected_data = AdditionalFileSerializer(additional_files, many=True).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_destroy_additional_file(client, additional_file):
    response = client.delete(reverse('additionalfile-detail', kwargs={'pk': additional_file.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not AdditionalFile.objects.filter(id=additional_file.id).exists()