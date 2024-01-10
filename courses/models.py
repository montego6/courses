from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth import get_user_model
import core.consts as consts
import courses.managers as cmanagers
from .validators import FileValidator

User = get_user_model()

COURSE_OPTION_CHOICES = [
    (consts.COURSE_OPTION_FREE, 'It is a free content'),
    (consts.COURSE_OPTION_BASIC, 'All the basic content'),
    (consts.COURSE_OPTION_EXTRA, 'Some additional files'),
    (consts.COURSE_OPTION_PREMIUM, 'All the content you need'),
]

COURSE_PAYMENT_CHOICES = [
    (consts.COURSE_PAYMENT_PAID, 'Course is paid'),
    (consts.COURSE_PAYMENT_NOT_PAID, 'Course is not paid'),
    (consts.COURSE_PAYMENT_ERROR, 'Course is not paid due to error'),
    (consts.COURSE_PAYMENT_REFUND, 'Course is refunded'),
]

validate_file = FileValidator(max_size=1024 * 100, 
                             content_types=('application/xml',))


class Course(models.Model):
    name = models.CharField(max_length=80, db_index=True)
    short_description = models.CharField(max_length=200, db_index=True)
    full_description = models.CharField(max_length=3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_courses')
    price = models.PositiveIntegerField(default=0)
    cover = models.ImageField(upload_to='media/courses/covers/')
    language = models.CharField(max_length=40)
    what_will_learn = ArrayField(models.CharField(max_length=120), size=20)
    requirements = ArrayField(models.CharField(max_length=60), size=12)
    options = models.JSONField()
    students = models.ManyToManyField(User, related_name='student_courses')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    subject = models.ForeignKey('categories.Subject', on_delete=models.SET_NULL, null=True, related_name='courses')

    objects = models.Manager()
    custom_objects = cmanagers.CourseManager()
    statistics = cmanagers.CourseStatisticsManager()


class StripeCourse(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='stripe')
    product = models.CharField(max_length=300)
    option_prices = models.JSONField()


class CoursePayment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    status = models.CharField(max_length=20, choices=COURSE_PAYMENT_CHOICES, default=consts.COURSE_PAYMENT_NOT_PAID)
    option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)


class Section(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')




