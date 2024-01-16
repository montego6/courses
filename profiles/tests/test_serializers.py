from unittest.mock import Mock
import pytest
import factory
from core.helpers import get_user_full_name
from courses.api.serializers import CourseSearchSerializer, CourseSerializer
from courses.tests.factories import CourseFactory, UserFactory
from profiles.models import TeacherProfile
from profiles.api.serializers import TeacherProfileSerializer
from profiles.tests import factories as ft
from courses.tests.conftest import disconnect_signals

@pytest.mark.django_db
def test_teacher_profile_serializer(teacher_profile):
    data = TeacherProfileSerializer(teacher_profile).data
    expected_data = {
       'id': teacher_profile.id,
       'avatar': teacher_profile.avatar.url,
       'bio': teacher_profile.bio,
       'balance': teacher_profile.balance,
       'name': get_user_full_name(teacher_profile.user),
       'rating': 0,
       'students': 0,
       'courses': [],
    }
    
    assert data == expected_data


@pytest.mark.django_db
def test_teacher_profile_serialize_data(user):
    data = factory.build(dict, FACTORY_CLASS=ft.TeacherProfileFactory)
    data['user'] = user.id
    serializer = TeacherProfileSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_question_test_serialize_data_fails():
    data = factory.build(dict, FACTORY_CLASS=ft.TeacherProfileFactory)
    del data['bio']
    serializer = TeacherProfileSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors != {}


@pytest.mark.django_db
def test_teacher_profile_serializer_create(user):
    data = factory.build(dict, FACTORY_CLASS=ft.TeacherProfileFactory)
    request = Mock()
    request.user = user
    context = {
        'request': request
    }
    serializer = TeacherProfileSerializer(data=data, context=context)
    assert serializer.is_valid()
    serializer.save()
    assert TeacherProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_teacher_profile_serializer_students(user, disconnect_signals):
    students = UserFactory.create_batch(9)
    course = CourseFactory(author=user)
    course.students.add(*students)
    profile = ft.TeacherProfileFactory(user=user)
    data = TeacherProfileSerializer(profile).data
    assert data['students'] == 9


@pytest.mark.django_db
def test_teacher_profile_serializer_courses(user, disconnect_signals):
    courses = CourseFactory.create_batch(9, author=user)
    profile = ft.TeacherProfileFactory(user=user)
    data = TeacherProfileSerializer(profile).data
    assert data['courses'] == CourseSearchSerializer(courses, many=True).data