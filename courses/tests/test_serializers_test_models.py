from unittest.mock import Mock
import factory
import pytest
import factories as ft
from courses.serializers import TestCompletionSerializer, TestQuestionSerializer, TestSerializer


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
        'id': test_completion.id,
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

