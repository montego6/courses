from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from courses.models import COURSE_OPTION_CHOICES, Section
from courses import consts


User = get_user_model()


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
    duration = models.PositiveIntegerField(null=True)
    section_items = GenericRelation(SectionItem)
    option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)
    

class AdditionalFile(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='extra_files')
    file = models.FileField(upload_to='media/courses/extra_files/')
    section_items = GenericRelation(SectionItem)
    option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)


class Test(models.Model):
    __test__ = False
    
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='tests')
    section_items = GenericRelation(SectionItem)
    option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)


class TestQuestion(models.Model):
    __test__ = False
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=180)
    options = ArrayField(models.CharField(max_length=100), size=3)
    answer = models.CharField(max_length=100)


class TestCompletion(models.Model):
    __test__ = False

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_completions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_completions')
    result = models.PositiveIntegerField()


class Homework(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    task = models.CharField(max_length=1000)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='homeworks')
    section_items = GenericRelation(SectionItem)
    option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)