from django.db.models import Q
import pytest
import factory
from django.urls import reverse
from rest_framework import status
from courses.models import Course
from courses.serializers import CourseSerializer, CourseSearchSerializer
import factories as ft


@pytest.mark.django_db
def test_list_course_search(client, disconnect_signals):
    query = 'ab'
    ft.CourseFactory.create_batch(64)
    courses = Course.objects.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(full_description__icontains=query))

    response = client.get(reverse('course-search') + f'?query={query}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == CourseSearchSerializer(courses, many=True).data