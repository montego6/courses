from django.contrib import admin

from sectionitems.models import AdditionalFile, Homework, Lesson, SectionItem, Test, TestQuestion

# Register your models here.
admin.site.register(AdditionalFile)
admin.site.register(Lesson)
admin.site.register(SectionItem)
admin.site.register(Test)
admin.site.register(TestQuestion)
admin.site.register(Homework)