import pytest
from rest_framework.test import APIClient
import categories.tests.factories as ft
from django.conf import settings

@pytest.fixture(autouse=True, scope='session')
def disable_logging():
    if 'core.middlewares.LogRequestsMiddleware' in settings.MIDDLEWARE:
        settings.MIDDLEWARE.remove('core.middlewares.LogRequestsMiddleware')

@pytest.fixture
def category():
    return ft.CategoryFactory()


@pytest.fixture
def subcategory():
    return ft.SubCategoryFactory()


@pytest.fixture
def subject():
    return ft.SubjectFactory()

@pytest.fixture
def client():
    return APIClient()