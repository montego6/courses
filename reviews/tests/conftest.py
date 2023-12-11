import pytest
from reviews.tests import factories as ft

@pytest.fixture
def review():
    return ft.ReviewFactory()