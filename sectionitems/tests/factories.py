import factory
from courses.tests.factories import SectionFactory, UserFactory
import sectionitems.models as models


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Lesson
    
    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    file = factory.django.FileField(from_path='media/media/courses/lessons/0.0_Введение.mp4')
    section = factory.SubFactory(SectionFactory)


class AdditinalFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdditionalFile

    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    file = factory.django.FileField(from_path='media/media/courses/extra_files/lord-of-the-rings.jpg')
    section = factory.SubFactory(SectionFactory)


class TestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Test
    
    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    section = factory.SubFactory(SectionFactory)


class TestQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TestQuestion

    test = factory.SubFactory(TestFactory)
    question = factory.Faker('text', max_nb_chars=70)
    options = factory.Faker('texts', nb_texts=3, max_nb_chars=70)
    answer = factory.LazyAttribute(lambda obj: obj.options[0])


class TestCompletionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TestCompletion

    test = factory.SubFactory(TestFactory)
    student = factory.SubFactory(UserFactory)
    result = 100


class HomeworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Homework

    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    task = factory.Faker('text', max_nb_chars=180)
    section = factory.SubFactory(SectionFactory)