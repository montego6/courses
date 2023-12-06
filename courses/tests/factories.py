from charset_normalizer import from_path
from django.db.migrations import questioner
import factory
from pytest import File
from courses import models
from categories.models import Subject, SubCategory, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user_%d" % n)
    password = factory.Faker('password', length=10)

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('text', max_nb_chars=20)

class SubCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubCategory
    
    name = factory.Faker('text', max_nb_chars=20)
    parent_category = factory.SubFactory(CategoryFactory)

class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject
    
    name = factory.Faker('text', max_nb_chars=20)
    parent_subcategory = factory.SubFactory(SubCategoryFactory)


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Course
        skip_postgeneration_save = True

    name = factory.Faker('text', max_nb_chars=70)
    short_description = factory.Faker('text', max_nb_chars=180)
    full_description = factory.Faker('text', max_nb_chars=1200)
    author = factory.SubFactory(UserFactory)
    price = 100
    cover = factory.django.ImageField(from_path='media/media/courses/covers/linux.jpg')
    language = factory.Faker('language_code')
    what_will_learn = factory.Faker('texts', nb_texts=8, max_nb_chars=60)
    requirements = factory.Faker('texts', nb_texts=6, max_nb_chars=60)
    options = factory.List([{"price": 1690, "option": "basic", "content": ["lesson"]}, 
                            {"price": 1900, "option": "extra"}, 
                            {"price": 2300, "option": "premium", "content": ["lesson", "test"]}])
    students = factory.RelatedFactoryList(UserFactory, size=5)
    subject = factory.SubFactory(SubjectFactory)

class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Section

    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    course = factory.SubFactory(CourseFactory)

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
    



