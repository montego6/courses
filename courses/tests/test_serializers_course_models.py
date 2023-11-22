from unittest.mock import Mock
import factory
import pytest
from courses.serializers import CourseProfileSerializer, CourseSearchSerializer, CourseSerializer, SectionSerializer
from factories import CourseFactory, SubjectFactory, UserFactory
from reviews.serializers import ReviewSerializer
import factories as ft


@pytest.mark.django_db
def test_course_serializer(course: CourseFactory):
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
def test_course_serialize_data(subject: SubjectFactory):
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
def test_course_serializer_create(subject: SubjectFactory, user: UserFactory):
    data = factory.build(dict, FACTORY_CLASS=ft.CourseFactory)
    data['subject'] = subject.id

    request = Mock()
    request.user = user
    serializer = CourseSerializer(data=data, context={'request': request})
    serializer.is_valid()
    course = serializer.save()
    assert course.author == user

@pytest.mark.django_db
def test_course_search_serializer(course: CourseFactory):
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
def test_course_profile_serializer(course: CourseFactory):
    data = CourseProfileSerializer(course).data
    expected_data = {
       'name': course.name,
       'short_description': course.short_description,
       'price': course.price,
       'cover': course.cover.url,
    }

    assert data == expected_data