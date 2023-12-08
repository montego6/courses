from django.urls import reverse
from rest_framework import status
import factory
from categories.models import Category, SubCategory
from categories.serializers import CategorySerializer, SubCategorySerializer
import categories.tests.factories as ft
import pytest



@pytest.mark.django_db
def test_create_subcategory(client, category):
    data = factory.build(dict, FACTORY_CLASS=ft.SubCategoryFactory, name='подкатегория')
    data['parent_category'] = category.id
    response = client.post(reverse('subcategory-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert SubCategory.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_update_subcategory(client, category, subcategory):
    data = factory.build(dict, FACTORY_CLASS=ft.SubCategoryFactory, name='подкатегория')
    data['parent_category'] = category.id
    response = client.put(reverse('subcategory-detail', kwargs={'pk': subcategory.id}), data)
    
    expected_data = {
        'id': subcategory.id,
        'name': data['name'],
        'parent_category': data['parent_category'],
        'subjects': [],
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_partial_update_subcategory(client, category, subcategory):
    data = {
        'parent_category': category.id
    }

    response = client.patch(reverse('subcategory-detail', kwargs={'pk': subcategory.id}), data)

    expected_data = {
        'id': subcategory.id,
        'name': subcategory.name,
        'parent_category': data['parent_category'],
        'subjects': [],
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_retrieve_subcategory(client, subcategory):
    response = client.get(reverse('subcategory-detail', kwargs={'pk': subcategory.id}))

    expected_data = SubCategorySerializer(subcategory).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_subcategory(client):
    subcategories = ft.SubCategoryFactory.create_batch(9)
    
    response = client.get(reverse('subcategory-list'))

    expected_data = SubCategorySerializer(subcategories, many=True).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_destroy_subcategory(client, subcategory):
    response = client.delete(reverse('subcategory-detail', kwargs={'pk': subcategory.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not SubCategory.objects.filter(id=subcategory.id).exists()