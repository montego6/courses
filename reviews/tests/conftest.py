import pytest
from reviews.tests import factories as ft
from django.conf import settings

@pytest.fixture
def review():
    return ft.ReviewFactory()

@pytest.fixture(autouse=True, scope='session')
def disable_logging():
    if 'core.middlewares.LogRequestsMiddleware' in settings.MIDDLEWARE:
        settings.MIDDLEWARE.remove('core.middlewares.LogRequestsMiddleware')