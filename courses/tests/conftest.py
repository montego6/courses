import pytest
from courses.models import Lesson, SectionItem, TestCompletion
from factories import CourseFactory, HomeworkFactory, LessonFactory, AdditinalFileFactory, SubjectFactory, TestCompletionFactory, TestFactory, TestQuestionFactory, SectionFactory, UserFactory



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
    questions = [TestQuestionFactory() for _ in range(5)]
    test = TestFactory()
    test.questions.set(questions)
    return test

@pytest.fixture
def test_question(disconnect_signals):
    return TestQuestionFactory()

@pytest.fixture
def test_completion(disconnect_signals):
    return TestCompletionFactory()

@pytest.fixture
def homework(disconnect_signals):
    return HomeworkFactory()

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

