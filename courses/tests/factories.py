from django.db.migrations import questioner
import factory
from courses import models
from categories.models import Subject, SubCategory, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user_%d" % n)

class CategoryFactory

class SubCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubCategory
    
    name = factory.Faker('text', max_nb_chars=20)
    parent_category = factory.SubFactory()

class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject
    
    name = factory.Faker('text', max_nb_chars=20)
    parent_subcategory = factory.SubFactory(SubCategoryFactory)


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Course

    name = factory.Faker('text', max_nb_chars=70)
    short_description = factory.Faker('text', max_nb_chars=180)
    full_description = factory.Faker('text', max_nb_chars=1200)
    author = factory.SubFactory(UserFactory)
    price = 100
    cover = factory.django.ImageField(from_path='media/media/courses/covers/linux.jpg')
    language = factory.Faker('language_code')
    what_will_learn = factory.Faker('texts', nb_texts=8, max_nb_chars=80)
    requirements = factory.Faker('texts', nb_texts=6, max_nb_chars=80)
    options = {
        "basic": {},
        "extra": {},
        "premium": {},
    }
    students = factory.RelatedFactoryList(UserFactory, size=5)
    subject = factory.SubFactory(SubjectFactory)

class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Section

    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    course = 

class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Lesson
    
    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    file = 'media/media/courses/lessons/0.0_Введение.mp4'
    section = factory.SubFactory(SectionFactory)


class AdditinalFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdditionalFile

    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    file = 'media/media/courses/extra_files/lord-of-the-rings.jpg'
    section = models.Section()


class TestQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TestQuestion

    test = models.Test()
    question = factory.Faker('text', max_nb_chars=70)
    options = factory.Faker('texts', nb_texts=3, max_nb_chars=70)
    answer = factory.LazyAttribute(lambda obj: obj.options[0])


class TestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Test
    
    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    questions = factory.RelatedFactoryList(TestQuestionFactory, size=5)
    # factory.LazyAttribute(lambda obj: obj.questions.set(TestQuestionFactory.build_batch(5)))
    # TestQuestionFactory.build_batch(5)
    section = models.Section()


