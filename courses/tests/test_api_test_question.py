from django.urls import reverse
from rest_framework import status
import factory
from courses.models import Test
from courses.serializers import TestQuestionSerializer
import factories as ft
import pytest



@pytest.mark.django_db
def test_create_test_question(client, test):
    data = factory.build(dict, FACTORY_CLASS=ft.TestQuestionFactory)
    data['test'] = test.id
    response = client.post(reverse('testquestion-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Test.objects.last() is not None


@pytest.mark.django_db
def test_update_test_question(client, test, test_question):
    data = factory.build(dict, FACTORY_CLASS=ft.TestQuestionFactory)
    data['test'] = test.id
    response = client.put(reverse('testquestion-detail', kwargs={'pk': test_question.id}), data)
    
    expected_data = {
        'id': test_question.id,
        'test': data['test'],
        'question': data['question'],
        'options': data['options'],
        'answer': data['answer'],
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_partial_update_test(client, test, test_question):
    data = {
        'question': 'test question',
        'test': test.id,
    }

    response = client.patch(reverse('testquestion-detail', kwargs={'pk': test_question.id}), data)

    expected_data = {
        'id': test_question.id,
        'test': data['test'],
        'question': data['question'],
        'options': test_question.options,
        'answer': test_question.answer,
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_retrieve_test_question(client, test_question):
    response = client.get(reverse('testquestion-detail', kwargs={'pk': test_question.id}))

    expected_data = TestQuestionSerializer(test_question).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_test_question(client, disconnect_signals):
    test_questions = ft.TestQuestionFactory.create_batch(9)
    
    response = client.get(reverse('testquestion-list'))

    expected_data = TestQuestionSerializer(test_questions, many=True).data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data