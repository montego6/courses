import pytest
from courses.serializers import AdditionalFileSerializer, LessonSerializer, TestQuestionSerializer, TestSerializer



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


@pytest.mark.django_db
def test_question_test_serializer(test_question):
    data = TestQuestionSerializer(test_question).data
    fields = {'id', 'test', 'question', 'options', 'answer'}
    assert set(data.keys()) == fields
    assert data['id'] == test_question.id
    assert data['test'] == test_question.test.id
    assert data['question'] == test_question.question
    assert data['options'] == test_question.options
    assert data['answer'] == test_question.answer


@pytest.mark.django_db
def test_test_serializer(test):
    data = TestSerializer(test).data
    fields = {'id', 'name', 'description', 'option', 'type'}
    assert set(data.keys()) == fields
    assert data['id'] == test.id
    assert data['name'] == test.name
    assert data['description'] == test.description
    assert data['option'] == test.option
    assert data['type'] == 'test'


@pytest.mark.django_db
def test_test_serializer_full(test):
    print(test.id)
    data = TestSerializer(test, context={'is_author': True}).data
    fields = {'id', 'name', 'description', 'option', 'type', 'questions', 'completed'}
    print(test.id)
    print(test.question)
    assert set(data.keys()) == fields
    assert data['id'] == test.id
    assert data['name'] == test.name
    assert data['description'] == test.description
    assert data['option'] == test.option
    # assert data['questions'] == TestQuestionSerializer(test.questions, many=True)
    assert data['completed'] == False
    assert data['type'] == 'test'