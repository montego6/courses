from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
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


class Section(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')


class SectionItem(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') 


class Lesson(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lessons')
    file = models.FileField(upload_to='media/courses/lessons/')
    section_items = GenericRelation(SectionItem)


class AdditionalFile(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='extra_files')
    file = models.FileField(upload_to='media/courses/extra_files/')
    section_items = GenericRelation(SectionItem)


class Test(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='tests')
    section_items = GenericRelation(SectionItem)


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=180)
    options = ArrayField(models.CharField(max_length=100), size=3)
    answer = models.CharField(max_length=100)


class Homework(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    task = models.CharField(max_length=1000)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='homeworks')
    section_items = GenericRelation(SectionItem)
