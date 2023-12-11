import pytest
import factory
from django.urls import reverse
from rest_framework import status
from courses.models import Section
from courses.serializers import SectionItemSerializer, SectionSerializer
import courses.tests.factories as ft



@pytest.mark.django_db
def test_create_section(client, course):
    data = factory.build(dict, FACTORY_CLASS=ft.SectionFactory)
    data['course'] = course.id
    response = client.post(reverse('section-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Section.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_update_section(client, course, section):
    data = factory.build(dict, FACTORY_CLASS=ft.SectionFactory)
    data['course'] = course.id
    response = client.put(reverse('section-detail', kwargs={'pk': section.id}), data)
    
    expected_data = {
        'id': section.id,
        'name': data['name'],
        'description': data['description'],
        'course': data['course'],
        'items': SectionItemSerializer(section.items, many=True).data
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_partial_update_section(client, course, section):
    data = {
        'name': 'test name',
        'course': course.id,
    }

    response = client.patch(reverse('section-detail', kwargs={'pk': section.id}), data)

    expected_data = {
        'id': section.id,
        'name': data['name'],
        'description': section.description,
        'course': data['course'],
        'items': SectionItemSerializer(section.items, many=True).data
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_retrieve_section(client, section):
    response = client.get(reverse('section-detail', kwargs={'pk': section.id}))

    expected_data = SectionSerializer(section).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_section(client, disconnect_signals):
    sections = ft.SectionFactory.create_batch(9)
    
    response = client.get(reverse('section-list'))

    expected_data = SectionSerializer(sections, many=True).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_destroy_section(client, section):
    response = client.delete(reverse('section-detail', kwargs={'pk': section.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Section.objects.filter(id=section.id).exists()