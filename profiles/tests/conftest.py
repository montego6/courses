import pytest
from profiles.tests.factories import TeacherProfileFactory
from courses.tests.factories import UserFactory
import os
import shutil
from django.conf import settings

@pytest.fixture(autouse=True, scope='session')
def disable_logging():
    if 'loggers.middlewares.LogRequestsMiddleware' in settings.MIDDLEWARE:
        settings.MIDDLEWARE.remove('loggers.middlewares.LogRequestsMiddleware')

@pytest.fixture(autouse=True, scope='session')
def delete_test_files():
    from django.conf import settings
    settings.MEDIA_ROOT = 'test_media/'
    yield
    if os.path.isdir(settings.MEDIA_ROOT):
        shutil.rmtree(settings.MEDIA_ROOT)


@pytest.fixture
def teacher_profile():
    return TeacherProfileFactory()

@pytest.fixture
def user():
    return UserFactory()


