from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField
# from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from courses.models import COURSE_OPTION_CHOICES, Section
from core import consts


User = get_user_model()


class SectionItem(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='items')
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    lesson = models.OneToOneField('Lesson', on_delete=models.CASCADE, blank=True, null=True)
    additional_file = models.OneToOneField('AdditionalFile', on_delete=models.CASCADE, blank=True, null=True)
    test = models.OneToOneField('Test', on_delete=models.CASCADE, blank=True, null=True)
    homework = models.OneToOneField('Homework', on_delete=models.CASCADE, blank=True, null=True)

    def clean(self) -> None:
        fields = [self.lesson, self.additional_file, self.test, self.homework]
        if sum([1 for field in fields if field]) != 1:
            raise ValidationError('One and only one section item type should be set')

    def __str__(self) -> str:
        return f'Section item for section with id={self.section.id}'
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=
            (
                Q(lesson__isnull=False) &
                Q(additional_file__isnull=True) &
                Q(test__isnull=True) &
                Q(homework__isnull=True)
            ) | 
            (
                Q(lesson__isnull=True) &
                Q(additional_file__isnull=False) &
                Q(test__isnull=True) &
                Q(homework__isnull=True)
            ) | 
            (
                Q(lesson__isnull=True) &
                Q(additional_file__isnull=True) &
                Q(test__isnull=False) &
                Q(homework__isnull=True)
            ) | 
            (
                Q(lesson__isnull=True) &
                Q(additional_file__isnull=True) &
                Q(test__isnull=True) &
                Q(homework__isnull=False)
            ), 
            name='only_one_not_null'
            )
        ]



class Item(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)

    class Meta:
        abstract = True


class Lesson(Item):
    file = models.FileField(upload_to='media/courses/lessons/')
    duration = models.PositiveIntegerField(null=True)
    
    def __str__(self) -> str:
        return f'Lesson with name={self.name} of section with id={self.section.id}'

class AdditionalFile(Item):
    # name = models.CharField(max_length=80)
    # description = models.CharField(max_length=200, null=True)
    # section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='extra_files')
    file = models.FileField(upload_to='media/courses/extra_files/')
    # section_items = GenericRelation(SectionItem)
    # option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)

    def __str__(self) -> str:
        return f'Additional file with name={self.name} of section with id={self.section.id} '

class Test(Item):
    __test__ = False
    
    # name = models.CharField(max_length=80)
    # description = models.CharField(max_length=200, null=True)
    # section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='tests')
    # section_items = GenericRelation(SectionItem)
    # option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)
    def __str__(self) -> str:
        return f'Test of section with id={self.section.id}'


class TestQuestion(models.Model):
    __test__ = False
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=180)
    options = ArrayField(models.CharField(max_length=100), size=3)
    answer = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'Test question of test with id={self.test.id} question={self.question}'


class TestCompletion(models.Model):
    __test__ = False

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_completions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_completions')
    result = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'Test completion of test with id={self.test.id} for student with id={self.student.id}'


class Homework(Item):
    # name = models.CharField(max_length=80)
    # description = models.CharField(max_length=200, null=True)
    task = models.CharField(max_length=1000)
    # section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='homeworks')
    # section_items = GenericRelation(SectionItem)
    # option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)

    def __str__(self) -> str:
        return f'Homework with name={self.name} of section with id={self.section.id}'