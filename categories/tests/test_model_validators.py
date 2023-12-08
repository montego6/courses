
import factory
import pytest
from categories.serializers import CategorySerializer, SubCategorySerializer, SubjectSerializer
import categories.tests.factories as ft


@pytest.mark.django_db
def test_subject_unique_validation(subject, subcategory):
    data = factory.build(dict, FACTORY_CLASS=ft.SubCategoryFactory, name=subject.name)
    data['parent_subcategory'] = subcategory.id
    serializer = SubjectSerializer(data=data)
    assert not serializer.is_valid()
    error_codes_set = set()
    for error in serializer.errors['name']:
       error_codes_set.add(error.code)
    assert 'unique' in error_codes_set


@pytest.mark.django_db
def test_subcategory_unique_validation(subcategory, category):
    data = factory.build(dict, FACTORY_CLASS=ft.SubCategoryFactory, name=subcategory.name)
    data['parent_category'] = category.id
    serializer = SubCategorySerializer(data=data)
    assert not serializer.is_valid()
    error_codes_set = set()
    for error in serializer.errors['name']:
       error_codes_set.add(error.code)
    assert 'unique' in error_codes_set


@pytest.mark.django_db
def test_category_unique_validation(category):
    data = factory.build(dict, FACTORY_CLASS=ft.SubCategoryFactory, name=category.name)
    serializer = CategorySerializer(data=data)
    assert not serializer.is_valid()
    error_codes_set = set()
    for error in serializer.errors['name']:
       error_codes_set.add(error.code)
    assert 'unique' in error_codes_set



@pytest.mark.parametrize('name', [
    'Asbest',
    '0123456',
    'asdморти',
    'Асмотритель1',
    'Фер',
    'Арь'
])
@pytest.mark.django_db
def test_subcategory_validate_name_fails(name, category):
    data = factory.build(dict, FACTORY_CLASS=ft.SubCategoryFactory, name=name)
    data['parent_category'] = category.id
    serializer = SubCategorySerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}


@pytest.mark.parametrize('name', [
    'Asbest',
    '0123456',
    'asdморти',
    'Асмотритель1',
    'Фер',
    'Арь'
])
@pytest.mark.django_db
def test_category_validate_name_fails(name):
    data = factory.build(dict, FACTORY_CLASS=ft.CategoryFactory, name=name)
    serializer = CategorySerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}