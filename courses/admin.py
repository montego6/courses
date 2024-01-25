from django.contrib import admin
from django.utils.http import urlencode
from django.urls import reverse
from django.utils.html import format_html
from .models import Course, Section, StripeCourse, CoursePayment

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'bname', 'author', 'subject', 'total_sales', 'show_students_link', 'is_published']
    list_display_links = ['id', 'bname']

    def bname(self, obj):
        return format_html('<b>{}</b>', obj.name)
    
    def show_students_link(self, obj):
        count = obj.num_students()
        url = reverse('admin:auth_user_changelist') + '?' + urlencode({'student_courses__id': obj.id})
        return format_html('<a href="{}">{} students</a>', url, count)

    bname.short_description = 'Name'
    show_students_link.short_description = 'Number of students'


admin.site.register(Course, CourseAdmin)
admin.site.register(Section)

admin.site.register(StripeCourse)
admin.site.register(CoursePayment)
# Register your models here.
