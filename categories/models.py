from django.db import models
from django.core.validators import MinLengthValidator,RegexValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(5, message='Количество символов должно быть больше 4'), 
                                                                    RegexValidator(r'[А-Яа-я]+')])


class SubCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(5, message='Количество символов должно быть больше 4'), 
                                                                    RegexValidator(r'[А-Яа-я]+')])
    parent_category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)


class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent_subcategory = models.ForeignKey(SubCategory, related_name='subjects', on_delete=models.CASCADE)