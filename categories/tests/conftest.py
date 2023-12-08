import pytest
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