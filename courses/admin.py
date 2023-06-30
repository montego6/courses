from django.contrib import admin
from .models import Course, Section, SectionItem, AdditionalFile, Lesson, Test, TestQuestion, Homework

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(AdditionalFile)
admin.site.register(Lesson)
admin.site.register(SectionItem)
admin.site.register(Test)
admin.site.register(TestQuestion)
admin.site.register(Homework)
# Register your models here.
