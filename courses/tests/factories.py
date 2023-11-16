import factory
from courses import models

class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Lesson
    
    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    file = 'media/media/courses/lessons/0.0_Введение.mp4'
    section = models.Section()


class AdditinalFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdditionalFile

    name = factory.Faker('text', max_nb_chars=70)
    description = factory.Faker('text', max_nb_chars=180)
    file = 'media/media/courses/extra_files/lord-of-the-rings.jpg'
    section = models.Section()