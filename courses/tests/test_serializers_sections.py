import pytest
import factory
from courses.models import SectionItem
from courses.serializers import AdditionalFileSerializer, HomeworkSerializer, LessonSerializer, SectionItemSerializer, SectionSerializer, TestSerializer
import courses.tests.factories as ft


@pytest.mark.parametrize('model, serializer', [
    (ft.LessonFactory, LessonSerializer),
    (ft.AdditinalFileFactory, AdditionalFileSerializer),
    (ft.TestFactory, TestSerializer),
    (ft.HomeworkFactory, HomeworkSerializer)
])
@pytest.mark.django_db
def test_section_item_serializer(disconnect_signals, model, serializer):
    section = ft.SectionFactory()
    instance = model()
    section_item = SectionItem.objects.create(content_object=instance, section=section)
    assert SectionItemSerializer(section_item).data == serializer(instance).data


@pytest.mark.django_db
def test_section_item_serializer_exception(disconnect_signals, course):
    section = ft.SectionFactory()
    section_item = SectionItem.objects.create(content_object=course, section=section)
    with pytest.raises(Exception):
        data = SectionItemSerializer(section_item).data


@pytest.mark.django_db
def test_section_serializer(section):
    data = SectionSerializer(section).data
    expected_data = {
       'id': section.id,
       'name': section.name,
       'description': section.description,
       'course': section.course.id,
       'items': SectionItemSerializer(section.items, many=True).data,
    }
    
    assert data == expected_data
    
@pytest.mark.django_db
def test_section_serialize_data(course):
    data = factory.build(dict, FACTORY_CLASS=ft.SectionFactory)
    data['course'] = course.id
    serializer = SectionSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_section_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.SectionFactory)
    del data['name']
    serializer = SectionSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}