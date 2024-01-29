from django.db.models import Q
import pytest
import factory
import json
from django.urls import reverse
from rest_framework import status
from courses.models import Course
from courses.api.serializers import CourseSerializer, CourseSearchSerializer, SectionSerializer
from reviews.api.serializers import ReviewSerializer
import courses.tests.factories as ft


@pytest.mark.django_db
def test_list_course_search(client, disconnect_signals):
    query = 'ab'
    ft.CourseFactory.create_batch(64)
    courses = Course.custom_objects.search_by_query(query)
    response = client.get(reverse('api:course-search') + f'?query={query}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == CourseSearchSerializer(courses, many=True, context={'request': response.wsgi_request}).data


@pytest.mark.django_db
def test_create_course(client_logged, subject):
    data = factory.build(dict, FACTORY_CLASS=ft.CourseFactory)
    data['subject'] = subject.id
    response = client_logged.post(reverse('api:course-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.filter(id=response.data['id']).exists()


@pytest.mark.django_db
def test_update_course(client, course, subject):
    data = factory.build(dict, FACTORY_CLASS=ft.CourseFactory)
    data['subject'] = subject.id
    response = client.put(reverse('api:course-detail', kwargs={'slug': course.slug}), data)
    
    expected_data = {
       'id': course.id,
       'name': data['name'],
       'short_description': data['short_description'],
       'full_description': data['full_description'],
       'author': course.author.id,
       'language': data['language'],
       'what_will_learn': data['what_will_learn'],
       'requirements': data['requirements'],
       'students': [student.id for student in course.students.all()],
       'date_created': str(course.date_created),
       'date_updated': str(course.date_updated),
       'is_published': course.is_published,
       'is_free': course.is_free,
       'subject': data['subject'],
       'sections': SectionSerializer(course.sections, many=True).data,
       'reviews': ReviewSerializer(course.reviews, many=True).data,
    }

    course.refresh_from_db()
    expected_data['cover'] = response.wsgi_request.build_absolute_uri(course.cover.url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data



@pytest.mark.django_db
def test_partial_update_course(client, course, subject):
    data = factory.build(dict, FACTORY_CLASS=ft.CourseFactory)
    data['subject'] = subject.id
    data.pop('name')
    data.pop('short_description')
    data.pop('full_description')
    data.pop('cover')
    response = client.patch(reverse('api:course-detail', kwargs={'slug': course.slug}), data)
    
    expected_data = {
       'id': course.id,
       'name': course.name,
       'short_description': course.short_description,
       'full_description': course.full_description,
       'cover': response.wsgi_request.build_absolute_uri(course.cover.url),
       'author': course.author.id,
       'language': data['language'],
       'what_will_learn': data['what_will_learn'],
       'requirements': data['requirements'],
       'students': [student.id for student in course.students.all()],
       'date_created': str(course.date_created),
       'date_updated': str(course.date_updated),
       'is_published': course.is_published,
       'is_free': course.is_free,
       'subject': data['subject'],
       'sections': SectionSerializer(course.sections, many=True).data,
       'reviews': ReviewSerializer(course.reviews, many=True).data,
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_retrieve_course(client, course):
    response = client.get(reverse('api:course-detail', kwargs={'slug': course.slug}))

    expected_data = CourseSerializer(course, context={'request': response.wsgi_request}).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_course(client, disconnect_signals):
    courses = ft.CourseFactory.create_batch(9)
    
    response = client.get(reverse('api:course-list'))

    expected_data = CourseSerializer(courses, many=True, context={'request': response.wsgi_request}).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_destroy_course(client, course):
    response = client.delete(reverse('api:course-detail', kwargs={'slug': course.slug}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Course.objects.filter(id=course.id).exists()