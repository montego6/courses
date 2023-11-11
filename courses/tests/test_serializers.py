import pytest
from unittest import TestCase
from courses.serializers import LessonSerializer



@pytest.mark.django_db
def test_lesson_serializer(lesson):
    data = LessonSerializer(lesson).data
    fields = {'id', 'name', 'description', 'duration', 'option', 'type'}
    assert set(data.keys()) == fields
    assert data['id'] == lesson.id
    assert data['name'] == lesson.name
    assert data['description'] == lesson.description
    assert data['duration'] == lesson.duration
    assert data['option'] == lesson.option
    assert data['type'] == 'lesson'


@pytest.mark.django_db
def test_lesson_serializer_full(lesson):
    data = LessonSerializer(lesson, context={'is_author': True}).data
    fields = {'id', 'name', 'description', 'duration', 'option', 'type', 'file', 'section'}
    assert set(data.keys()) == fields
    assert data['id'] == lesson.id
    assert data['name'] == lesson.name
    assert data['description'] == lesson.description
    assert data['duration'] == lesson.duration
    assert data['option'] == lesson.option
    assert data['file'] == lesson.file.url
    assert data['section'] == lesson.section.id
    assert data['type'] == 'lesson'