import pytest
import factory
from courses.api.serializers import SectionSerializer
import courses.tests.factories as ft
from sectionitems.api.serializers import SectionItemSerializer





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