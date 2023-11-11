import pytest
from model_bakery import baker
from courses.models import Lesson



@pytest.fixture
def disconnect_signals(monkeypatch):
    monkeypatch.setattr('django.db.models.signals.post_save.send', lambda **kwargs: True)

@pytest.fixture
def lesson(disconnect_signals):
    return baker.make(Lesson, file='/media/courses/covers/linux.jpg')

