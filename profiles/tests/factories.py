import factory
from profiles import models
from courses.tests.factories import UserFactory

class TeacherProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TeacherProfile
        skip_postgeneration_save = True

    avatar = factory.django.ImageField(from_path='media/media/courses/covers/linux.jpg')
    bio = factory.Faker('text', max_nb_chars=2000)
    user = factory.SubFactory(UserFactory)
    balance = 100
