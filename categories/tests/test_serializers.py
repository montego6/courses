import pytest
import factory
import categories.tests.factories as ft
from categories.serializers import CategorySerializer, SubCategorySerializer, SubjectSerializer


@pytest.mark.django_db
def test_subject_serializer(subject):
    data = SubjectSerializer(subject).data
    expected_data = {
        'id': subject.id,
        'name': subject.name,
        'parent_subcategory': subject.parent_subcategory.id
    }

    assert data == expected_data


@pytest.mark.django_db
def test_subject_serialize_data(subcategory):
    data = factory.build(dict, FACTORY_CLASS=ft.SubjectFactory)
    data['parent_subcategory'] = subcategory.id
    serializer = SubjectSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


@pytest.mark.django_db
def test_subject_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.SubjectFactory)
    serializer = SubjectSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}



pass

@pytest.mark.django_db
def test_subcategory_serializer(subcategory):
    data = SubCategorySerializer(subcategory).data
    expected_data = {
        'id': subcategory.id,
        'name': subcategory.name,
        'parent_category': subcategory.parent_category.id,
        'subjects': SubjectSerializer(subcategory.subjects, many=True).data
    }

    assert data == expected_data


@pytest.mark.django_db
def test_subcategory_serialize_data(category):
    data = factory.build(dict, FACTORY_CLASS=ft.SubCategoryFactory, name='Подкатегория')
    data['parent_category'] = category.id
    serializer = SubCategorySerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


@pytest.mark.django_db
def test_subcategory_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.SubCategoryFactory)
    serializer = SubCategorySerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}


pass

@pytest.mark.django_db
def test_category_serializer(category):
    data = CategorySerializer(category).data
    expected_data = {
        'id': category.id,
        'name': category.name,
        'subcategories': SubCategorySerializer(category.subcategories, many=True).data
    }

    assert data == expected_data


@pytest.mark.django_db
def test_category_serialize_data():
    data = factory.build(dict, FACTORY_CLASS=ft.CategoryFactory, name='Категория')
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


@pytest.mark.django_db
def test_category_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.CategoryFactory)
    data.pop('name')
    serializer = SubCategorySerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}