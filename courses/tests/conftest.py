import pytest
from courses.models import Lesson
from factories import LessonFactory, AdditinalFileFactory, TestFactory, TestQuestionFactory



@pytest.fixture
def disconnect_signals(monkeypatch):
    monkeypatch.setattr('django.db.models.signals.post_save.send', lambda **kwargs: True)

@pytest.fixture
def lesson(disconnect_signals):
    return LessonFactory()

@pytest.fixture
def additional_file(disconnect_signals):
    return AdditinalFileFactory()

@pytest.fixture
def test(disconnect_signals):
    return TestFactory()

@pytest.fixture
def test_question():
    return TestQuestionFactory()

