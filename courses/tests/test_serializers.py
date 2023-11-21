from unittest.mock import Mock
from django.test import RequestFactory
import pytest
import factory
from rest_framework.request import Request
from courses.models import SectionItem, TestCompletion
import factories as ft
from courses.serializers import AdditionalFileSerializer, CourseProfileSerializer, CourseSerializer, HomeworkSerializer, LessonSerializer, SectionItemSerializer, SectionSerializer, TestCompletionSerializer, TestQuestionSerializer, TestSerializer, CourseSearchSerializer
from reviews.serializers import ReviewSerializer



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


def test_lesson_serialize_data():
    data = factory.build(dict, FACTORY_CLASS=ft.LessonFactory)
    serializer = LessonSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_lesson_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.LessonFactory)
    del data['name']
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


def test_additional_file_serialize_data():
    data = factory.build(dict, FACTORY_CLASS=ft.AdditinalFileFactory)
    serializer = AdditionalFileSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_additional_file_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.AdditinalFileFactory)
    del data['name']
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
def test_question_test_serializer_model(test_question):
    data = TestQuestionSerializer(test_question).data
    expected_data = {
       'id': test_question.id,
       'test': test_question.test.id,
       'question': test_question.question,
       'options': test_question.options,
       'answer': test_question.answer,
    }
    
    assert data == expected_data


@pytest.mark.django_db
def test_question_test_serialize_data(test):
    data = factory.build(dict, FACTORY_CLASS=ft.TestQuestionFactory)
    data['test'] = test.id
    serializer = TestQuestionSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_question_test_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.TestQuestionFactory)
    del data['question']
    serializer = TestQuestionSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}


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


def test_test_serialize_data():
    data = factory.build(dict, FACTORY_CLASS=ft.TestFactory)
    serializer = TestSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_test_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.TestFactory)
    del data['name']
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
def test_test_serializer_completion(test_completion):
    user, test = test_completion.student, test_completion.test
    data_with_user_context = TestSerializer(test, context={'is_author': True, 'user': user.id}).data
    data_without_user_context = TestSerializer(test, context={'is_author': True}).data
    assert data_with_user_context['completed'] == 100
    assert data_without_user_context['completed'] == False

@pytest.mark.django_db
def test_test_completion_serializer_user(user, test):
    data = factory.build(dict, FACTORY_CLASS=ft.TestCompletionFactory)
    data['test'] = test.id

    request = Mock()
    request.user = user
    serializer = TestCompletionSerializer(data=data, context={'request': request})
    serializer.is_valid()
    test_completion = serializer.save()
    assert test_completion.student == user

@pytest.mark.django_db
def test_test_completion_serializer(test_completion):
    data = TestCompletionSerializer(test_completion).data
    expected_data = {
        'test': test_completion.test.id,
        'result': test_completion.result,
    }

    assert data == expected_data


@pytest.mark.django_db
def test_test_completion_serialize_data(test):
    data = factory.build(dict, FACTORY_CLASS=ft.TestCompletionFactory)
    data['test'] = test.id
    serializer = TestCompletionSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_test_completion_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.TestCompletionFactory)
    del data['test']
    serializer = TestCompletionSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}


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


def test_homework_serialize_data():
    data = factory.build(dict, FACTORY_CLASS=ft.HomeworkFactory)
    serializer = HomeworkSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_homework_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.HomeworkFactory)
    del data['name']
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

@pytest.mark.django_db
def test_course_serializer(course):
    data = CourseSerializer(course).data
    expected_data = {
       'id': course.id,
       'name': course.name,
       'short_description': course.short_description,
       'full_description': course.full_description,
       'author': course.author.id,
       'price': course.price,
       'cover': course.cover.url,
       'language': course.language,
       'what_will_learn': course.what_will_learn,
       'requirements': course.requirements,
       'options': course.options,
       'students': [student.id for student in course.students.all()],
       'date_created': str(course.date_created),
       'date_updated': str(course.date_updated),
       'is_published': course.is_published,
       'is_free': course.is_free,
       'subject': course.subject.id,
       'sections': SectionSerializer(course.sections, many=True).data,
       'reviews': ReviewSerializer(course.reviews, many=True).data,
    }

    assert data == expected_data

@pytest.mark.django_db
def test_course_serialize_data(subject):
    data = factory.build(dict, FACTORY_CLASS=ft.CourseFactory)
    data['subject'] = subject.id
    serializer = CourseSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_section_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.CourseFactory)
    del data['name']
    serializer = CourseSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}

@pytest.mark.django_db
def test_course_serializer_create(subject, user):
    data = factory.build(dict, FACTORY_CLASS=ft.CourseFactory)
    data['subject'] = subject.id

    request = Mock()
    request.user = user
    serializer = CourseSerializer(data=data, context={'request': request})
    serializer.is_valid()
    course = serializer.save()
    assert course.author == user

@pytest.mark.django_db
def test_course_search_serializer(course):
    data = CourseSearchSerializer(course).data
    expected_data = {
       'id': course.id,
       'name': course.name,
       'short_description': course.short_description,
       'author': {'id': course.author.id, 'name': course.author.first_name + ' ' + course.author.last_name},
       'price': course.price,
       'duration': 0,
       'rating': 0,
       'cover': course.cover.url,
       'language': course.language,
       'options': [],
       'students': course.students.count(),
       'subject': course.subject.name,
    }

    assert data == expected_data


@pytest.mark.django_db
def test_course_profile_serializer(course):
    data = CourseProfileSerializer(course).data
    expected_data = {
       'name': course.name,
       'short_description': course.short_description,
       'price': course.price,
       'cover': course.cover.url,
    }

    assert data == expected_data