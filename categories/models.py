from django.db import models
from django.core.validators import MinLengthValidator,RegexValidator

from categories.managers import CategoryStatisticsManager

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(5, message='Количество символов должно быть больше 4'), 
                                                                    RegexValidator(r'^[А-Яа-я\-]+$', message='Допускаются только кириллические буквы')])
    
    objects = models.Manager()
    statistics = CategoryStatisticsManager()

    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(5, message='Количество символов должно быть больше 4'), 
                                                                    RegexValidator(r'^[А-Яа-я\-]+$', message='Допускаются только кириллические буквы')])
    parent_category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name}, категория: {self.parent_category.name}'


class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent_subcategory = models.ForeignKey(SubCategory, related_name='subjects', on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f'{self.name}, подкатегория: {self.parent_subcategory.name}'