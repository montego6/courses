from django.contrib import admin
from .models import Course, Section, SectionItem, AdditionalFile, Lesson

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(AdditionalFile)
admin.site.register(Lesson)
admin.site.register(SectionItem)
# Register your models here.
