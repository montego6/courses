import pytest
from courses.serializers import AdditionalFileSerializer, LessonSerializer



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
    print(data)
    assert set(data.keys()) == fields
    assert data['id'] == lesson.id
    assert data['name'] == lesson.name
    assert data['description'] == lesson.description
    assert data['duration'] == lesson.duration
    assert data['option'] == lesson.option
    assert data['file'] == lesson.file.url
    assert data['section'] == lesson.section.id
    assert data['type'] == 'lesson'


@pytest.mark.django_db
def test_additional_file_serializer(additional_file):
    data = AdditionalFileSerializer(additional_file).data
    fields = {'id', 'name', 'description', 'option', 'type'}
    assert set(data.keys()) == fields
    assert data['id'] == additional_file.id
    assert data['name'] == additional_file.name
    assert data['description'] == additional_file.description
    assert data['option'] == additional_file.option
    assert data['type'] == 'extra_file'


@pytest.mark.django_db
def test_additional_file_serializer_full(additional_file):
    data = AdditionalFileSerializer(additional_file, context={'is_author': True}).data
    fields = {'id', 'name', 'description', 'option', 'type', 'file', 'section'}
    assert set(data.keys()) == fields
    assert data['id'] == additional_file.id
    assert data['name'] == additional_file.name
    assert data['description'] == additional_file.description
    assert data['option'] == additional_file.option
    assert data['file'] == additional_file.file.url
    assert data['section'] == additional_file.section.id
    assert data['type'] == 'extra_file'