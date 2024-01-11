import factory
from courses import models
from categories.tests.factories import SubjectFactory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user_%d" % n)
    password = factory.Faker('password', length=10)




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


    



