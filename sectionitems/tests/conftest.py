import pytest
from rest_framework.test import APIClient
import shutil
import os
from courses.tests.factories import SectionFactory, UserFactory
from sectionitems.models import SectionItem
from django.conf import settings
from sectionitems.tests.factories import AdditinalFileFactory, HomeworkFactory, LessonFactory, TestCompletionFactory, TestFactory, TestQuestionFactory


@pytest.fixture(autouse=True, scope='session')
def disable_logging():
    if 'core.middlewares.LogRequestsMiddleware' in settings.MIDDLEWARE:
        settings.MIDDLEWARE.remove('core.middlewares.LogRequestsMiddleware')

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
    if os.path.isdir(settings.MEDIA_ROOT):
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
def user():
    return UserFactory()