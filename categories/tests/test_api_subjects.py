from django.urls import reverse
from rest_framework import status
import factory
from categories.models import Category, SubCategory, Subject
from categories.serializers import CategorySerializer, SubCategorySerializer, SubjectSerializer
import categories.tests.factories as ft
import pytest



@pytest.mark.django_db
def test_create_subject(client, subcategory):
    data = factory.build(dict, FACTORY_CLASS=ft.SubjectFactory)
    data['parent_subcategory'] = subcategory.id
    response = client.post(reverse('subject-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Subject.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_update_subject(client, subject, subcategory):
    data = factory.build(dict, FACTORY_CLASS=ft.SubjectFactory)
    data['parent_subcategory'] = subcategory.id
    response = client.put(reverse('subject-detail', kwargs={'pk': subject.id}), data)
    
    expected_data = {
        'id': subject.id,
        'name': data['name'],
        'parent_subcategory': data['parent_subcategory'],
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_partial_update_subject(client, subject, subcategory):
    data = {
        'parent_subcategory': subcategory.id
    }

    response = client.patch(reverse('subject-detail', kwargs={'pk': subject.id}), data)

    expected_data = {
        'id': subject.id,
        'name': subject.name,
        'parent_subcategory': data['parent_subcategory'],
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_retrieve_subject(client, subject):
    response = client.get(reverse('subject-detail', kwargs={'pk': subject.id}))

    expected_data = SubjectSerializer(subject).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_subject(client):
    subjects = ft.SubjectFactory.create_batch(9)
    
    response = client.get(reverse('subject-list'))

    expected_data = SubjectSerializer(subjects, many=True).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_destroy_subject(client, subject):
    response = client.delete(reverse('subject-detail', kwargs={'pk': subject.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Subject.objects.filter(id=subject.id).exists()