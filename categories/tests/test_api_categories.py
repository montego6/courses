from django.urls import reverse
from rest_framework import status
import factory
from categories.models import Category
from categories.api.serializers import CategorySerializer
import categories.tests.factories as ft
import pytest





@pytest.mark.django_db
def test_create_category(client):
    data = factory.build(dict, FACTORY_CLASS=ft.CategoryFactory, name='категория')
    response = client.post(reverse('api:category-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_update_category(client, category):
    data = factory.build(dict, FACTORY_CLASS=ft.CategoryFactory, name='категория')
    response = client.put(reverse('api:category-detail', kwargs={'pk': category.id}), data)
    
    expected_data = {
        'id': category.id,
        'name': data['name'],
        'subcategories': [],
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_partial_update_category(client, category):
    data = {
        'name': 'категория'
    }

    response = client.patch(reverse('api:category-detail', kwargs={'pk': category.id}), data)

    expected_data = {
        'id': category.id,
        'name': data['name'],
        'subcategories': [],
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_retrieve_category(client, category):
    response = client.get(reverse('api:category-detail', kwargs={'pk': category.id}))

    expected_data = CategorySerializer(category).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_category(client):
    categories = ft.CategoryFactory.create_batch(9)
    
    response = client.get(reverse('api:category-list'))

    expected_data = CategorySerializer(categories, many=True).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_destroy_category(client, category):
    response = client.delete(reverse('api:category-detail', kwargs={'pk': category.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Category.objects.filter(id=category.id).exists()