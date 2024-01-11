from unittest.mock import Mock
import pytest
import factory
from courses.tests.factories import CourseFactory
from sectionitems.api.serializers import AdditionalFileSerializer, HomeworkSerializer, LessonSerializer, SectionItemSerializer, TestQuestionSerializer, TestSerializer
from sectionitems.models import SectionItem
import sectionitems.tests.factories as ft


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
def test_section_item_serializer_exception(disconnect_signals):
    course = CourseFactory()
    section = ft.SectionFactory()
    section_item = SectionItem.objects.create(content_object=course, section=section)
    with pytest.raises(Exception):
        data = SectionItemSerializer(section_item).data


@pytest.mark.django_db
def test_lesson_serialize_model(lesson):
    data = LessonSerializer(lesson).data
    expected_data = {
       'id': lesson.id,
       'name': lesson.name,
       'description': lesson.description,
       'duration': lesson.duration,
       'option': lesson.option,
       'type': 'lesson',
    }
    
    assert data == expected_data

@pytest.mark.django_db
def test_lesson_serialize_data(section):
    data = factory.build(dict, FACTORY_CLASS=ft.LessonFactory)
    data['section'] = section.id
    serializer = LessonSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_lesson_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.LessonFactory)
    serializer = LessonSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}


@pytest.mark.django_db
def test_lesson_serializer_full(lesson):
    data = LessonSerializer(lesson, context={'is_author': True}).data
    expected_data = {
       'id': lesson.id,
       'name': lesson.name,
       'description': lesson.description,
       'duration': lesson.duration,
       'option': lesson.option,
       'file': lesson.file.url,
       'section': lesson.section.id,
       'type': 'lesson',
    }
    
    assert data == expected_data


@pytest.mark.django_db
def test_additional_file_serializer_model(additional_file):
    data = AdditionalFileSerializer(additional_file).data
    expected_data = {
       'id': additional_file.id,
       'name': additional_file.name,
       'description': additional_file.description,
       'option': additional_file.option,
       'type': 'extra_file',
    }
    
    assert data == expected_data

@pytest.mark.django_db
def test_additional_file_serialize_data(section):
    data = factory.build(dict, FACTORY_CLASS=ft.AdditinalFileFactory)
    data['section'] = section.id
    serializer = AdditionalFileSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_additional_file_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.AdditinalFileFactory)
    serializer = AdditionalFileSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}


@pytest.mark.django_db
def test_additional_file_serializer_full(additional_file):
    data = AdditionalFileSerializer(additional_file, context={'is_author': True}).data
    expected_data = {
       'id': additional_file.id,
       'name': additional_file.name,
       'description': additional_file.description,
       'option': additional_file.option,
       'file': additional_file.file.url,
       'section': additional_file.section.id,
       'type': 'extra_file',
    }
    
    assert data == expected_data





@pytest.mark.django_db
def test_test_serializer(test):
    data = TestSerializer(test).data
    expected_data = {
       'id': test.id,
       'name': test.name,
       'description': test.description,
       'option': test.option,
       'type': 'test',
    }
    
    assert data == expected_data

@pytest.mark.django_db
def test_test_serialize_data(section):
    data = factory.build(dict, FACTORY_CLASS=ft.TestFactory)
    data['section'] = section.id
    serializer = TestSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_test_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.TestFactory)
    serializer = TestSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}


@pytest.mark.django_db
def test_test_serializer_full(test):
    data = TestSerializer(test, context={'is_author': True}).data
    expected_data = {
       'id': test.id,
       'name': test.name,
       'description': test.description,
       'option': test.option,
       'questions': TestQuestionSerializer(test.questions, many=True).data,
       'section': test.section.id,
       'type': 'test',
       'completed': False,
    }
    
    assert data == expected_data





@pytest.mark.django_db
def test_homework_serializer(homework):
    data = HomeworkSerializer(homework).data
    expected_data = {
       'id': homework.id,
       'name': homework.name,
       'description': homework.description,
       'option': homework.option,
       'type': 'homework',
    }
    
    assert data == expected_data


@pytest.mark.django_db
def test_homework_serialize_data(section):
    data = factory.build(dict, FACTORY_CLASS=ft.HomeworkFactory)
    data['section'] = section.id
    serializer = HomeworkSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_homework_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.HomeworkFactory)
    serializer = HomeworkSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}


@pytest.mark.django_db
def test_homework_serializer_full(homework):
    data = HomeworkSerializer(homework, context={'is_author': True}).data
    expected_data = {
       'id': homework.id,
       'name': homework.name,
       'description': homework.description,
       'task': homework.task,
       'section': homework.section.id,
       'option': homework.option,
       'type': 'homework',
    }
    
    assert data == expected_data