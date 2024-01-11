import pytest
from django.conf import settings
from rest_framework.test import APIClient
from categories.tests.factories import SubjectFactory
from courses.tests.factories import CourseFactory, SectionFactory, UserFactory
import shutil
import os
from sectionitems.models import SectionItem

from sectionitems.tests.factories import LessonFactory, TestFactory


@pytest.fixture(autouse=True, scope='session')
def disable_logging():
    if 'loggers.middlewares.LogRequestsMiddleware' in settings.MIDDLEWARE:
        settings.MIDDLEWARE.remove('loggers.middlewares.LogRequestsMiddleware')

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

