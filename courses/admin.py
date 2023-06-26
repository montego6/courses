from django.contrib import admin
from .models import Course, Section, SectionItem, AdditionalFile, Lesson, Test, TestQuestion

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(AdditionalFile)
admin.site.register(Lesson)
admin.site.register(SectionItem)
admin.site.register(Test)
admin.site.register(TestQuestion)
# Register your models here.
