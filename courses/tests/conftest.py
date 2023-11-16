import pytest
from courses.models import Lesson
from factories import LessonFactory, AdditinalFileFactory



@pytest.fixture
def disconnect_signals(monkeypatch):
    monkeypatch.setattr('django.db.models.signals.post_save.send', lambda **kwargs: True)

@pytest.fixture
def lesson(disconnect_signals):
    return LessonFactory.build()

@pytest.fixture
def additional_file(disconnect_signals):
    return AdditinalFileFactory.build()

