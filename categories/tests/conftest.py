import pytest
from rest_framework.test import APIClient
import categories.tests.factories as ft

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