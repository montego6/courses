from asyncio import shield
import pytest
from rest_framework.test import APIClient
from courses.models import Lesson, SectionItem, TestCompletion
from factories import CourseFactory, HomeworkFactory, LessonFactory, AdditinalFileFactory, SubjectFactory, TestCompletionFactory, TestFactory, TestQuestionFactory, SectionFactory, UserFactory
import os
import shutil


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def client_logged(user):
    client = APIClient()
    password = user.password
    user.set_password(user.password)
    user.save()
    client.login(username=user.username, password=password)
    yield client
    client.logout()

@pytest.fixture
def disconnect_signals(monkeypatch):
    monkeypatch.setattr('django.db.models.signals.post_save.send', lambda **kwargs: True)

@pytest.fixture(autouse=True, scope='session')
def delete_test_files():
    from django.conf import settings
    settings.MEDIA_ROOT = 'test_media/'
    yield
    shutil.rmtree(settings.MEDIA_ROOT)

@pytest.fixture
def lesson(disconnect_signals):
    return LessonFactory()


@pytest.fixture
def additional_file(disconnect_signals):
    return AdditinalFileFactory()

@pytest.fixture
def test(disconnect_signals):
    questions = [TestQuestionFactory() for _ in range(5)]
    test = TestFactory()
    test.questions.set(questions)
    return test

@pytest.fixture
def test_question(disconnect_signals):
    return TestQuestionFactory()

@pytest.fixture
def test_completion(disconnect_signals):
    return TestCompletionFactory()

@pytest.fixture
def homework(disconnect_signals):
    return HomeworkFactory()

@pytest.fixture
def section(disconnect_signals):
    section = SectionFactory()
    items = [LessonFactory(), TestFactory(), LessonFactory()]
    section_items = [SectionItem.objects.create(content_object=item, section=section) for item in items]
    return section

@pytest.fixture
def course(disconnect_signals):
    return CourseFactory()

@pytest.fixture
def subject(disconnect_signals):
    return SubjectFactory()
    
@pytest.fixture
def user():
    return UserFactory()

