from django.contrib import admin
from .models import Course, Section, StripeCourse, CoursePayment

admin.site.register(Course)
admin.site.register(Section)

admin.site.register(StripeCourse)
admin.site.register(CoursePayment)
# Register your models here.
