from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    name = models.CharField(max_length=80, db_index=True)
    short_description = models.CharField(max_length=200, db_index=True)
    full_description = models.CharField(max_length=3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_courses')
    price = models.PositiveIntegerField()
    cover = models.ImageField(upload_to='media/courses/covers/')
    language = models.CharField(max_length=40)
    what_will_learn = ArrayField(models.CharField(max_length=40), size=20)
    requirements = ArrayField(models.CharField(max_length=60), size=12)
    options = models.JSONField()
    students = models.ManyToManyField(User, related_name='student_courses')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=False)
