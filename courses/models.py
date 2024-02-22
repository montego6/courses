from email.policy import default
from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth import get_user_model
import core.consts as consts
import courses.managers as cmanagers
from users.helpers import get_user_full_name
from .validators import FileValidator
import statistic.managers 

User = get_user_model()

COURSE_OPTION_CHOICES = [
    (consts.COURSE_OPTION_FREE, 'Free: it is a free content'),
    (consts.COURSE_OPTION_BASIC, 'Basic: all the basic content'),
    (consts.COURSE_OPTION_EXTRA, 'Extra: some additional files'),
    (consts.COURSE_OPTION_PREMIUM, 'Premium: all the content you need'),
]

COURSE_PAYMENT_CHOICES = [
    (consts.COURSE_PAYMENT_PAID, 'Course is paid'),
    (consts.COURSE_PAYMENT_NOT_PAID, 'Course is not paid'),
    (consts.COURSE_PAYMENT_ERROR, 'Course is not paid due to error'),
    (consts.COURSE_PAYMENT_REFUND, 'Course is refunded'),
]

COURSE_LEVEL_CHOICES = [
    (consts.COURSE_LEVEL_BEGINNER, 'Beginner level'),
    (consts.COURSE_LEVEL_ADVANCED, 'Advanced level'),
    (consts.COURSE_LEVEL_EXPERT, 'Expert level'),
]

validate_file = FileValidator(max_size=1024 * 100, 
                             content_types=('application/xml',))


class Course(models.Model):
    __prev_name = None
    
    name = models.CharField(max_length=80, db_index=True)
    short_description = models.CharField(max_length=200, db_index=True)
    full_description = models.CharField(max_length=3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_courses')
    # price = models.PositiveIntegerField(default=0)
    cover = models.ImageField(upload_to='media/courses/covers/')
    language = models.CharField(max_length=40)
    what_will_learn = ArrayField(models.CharField(max_length=120), size=20)
    requirements = ArrayField(models.CharField(max_length=60), size=12)
    # options = ArrayField(models.CharField(max_length=12), size=3)
    students = models.ManyToManyField(User, related_name='student_courses')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    subject = models.ForeignKey('categories.Subject', on_delete=models.SET_NULL, null=True, related_name='courses')
    slug = models.SlugField(max_length=160, unique=True, null=True)
    level = models.CharField(max_length=16, choices=COURSE_LEVEL_CHOICES, default=consts.COURSE_LEVEL_BEGINNER)

    objects = models.Manager()
    custom_objects = cmanagers.CourseManager()
    
    
    statistics = statistic.managers.CourseStatisticsManager()

    def __str__(self) -> str:
        return f'{self.name} by {get_user_full_name(self.author)}'
    
    def total_sales(self):
        from django.db.models import Sum
        result = CoursePayment.objects.filter(course=self).aggregate(Sum('amount'))
        return result['amount__sum']
    
    def num_students(self):
        return self.students.count()


class CoursePrice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='prices')
    amount = models.PositiveIntegerField()
    stripe = models.CharField(max_length=64, blank=True, null=True)
    option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)

    def __str__(self) -> str:
        return f'Price for course with id={self.course.id} and option {self.option}'


class CourseUpgradePrice(models.Model):
    class UpgradeFrom(models.TextChoices):
        BASIC = consts.COURSE_OPTION_BASIC, 'All the basic content'
        EXTRA = consts.COURSE_OPTION_EXTRA, 'Some additional files'
    
    class UpgradeTo(models.TextChoices):
        EXTRA = consts.COURSE_OPTION_EXTRA, 'Some additional files'
        PREMIUM = consts.COURSE_OPTION_PREMIUM, 'All the content you need'

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='upgrades')
    amount = models.PositiveIntegerField()
    stripe = models.CharField(max_length=64)
    stripe_product = models.CharField(max_length=64)
    from_option = models.CharField(max_length=20, choices=UpgradeFrom.choices, default=UpgradeFrom.BASIC)
    to_option = models.CharField(max_length=20, choices=UpgradeTo.choices, default=UpgradeTo.EXTRA)

    def __str__(self) -> str:
        return f'Upgrade for course id={self.course.id} from option {self.from_option} to option {self.to_option}'


class StripeCourse(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='stripe')
    product = models.CharField(max_length=300)
    # option_prices = models.JSONField()

    def __str__(self) -> str:
        return f'Stripe for course id={self.course.id}'


class CoursePayment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    status = models.CharField(max_length=20, choices=COURSE_PAYMENT_CHOICES, default=consts.COURSE_PAYMENT_NOT_PAID)
    option = models.CharField(max_length=20, choices=COURSE_OPTION_CHOICES, default=consts.COURSE_OPTION_BASIC)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Payment for course id={self.course.id} by student id={self.student.id} option {self.option}'


class Section(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')

    def __str__(self) -> str:
        return f'Section for course id={self.course.id} with name={self.name}'




