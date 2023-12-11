import factory
from reviews import models
from courses.tests.factories import UserFactory, CourseFactory

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Review
        skip_postgeneration_save = True

    course = factory.SubFactory(CourseFactory)
    student = factory.SubFactory(UserFactory)
    comment = factory.Faker('text', max_nb_chars=400)
    rating = 5