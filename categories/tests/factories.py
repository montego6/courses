import factory

from categories.models import Category, SubCategory, Subject

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