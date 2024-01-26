from django.contrib import admin
from django.utils.http import urlencode
from django.urls import reverse
from django.utils.html import format_html

from users.helpers import get_user_full_name
from .models import Course, CoursePrice, CourseUpgradePrice, Section, StripeCourse, CoursePayment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'bname', 'author_fullname_link', 'author_id', 'subject', 'total_sales', 'show_students_link', 'is_published']
    list_display_links = ['id', 'bname']
    list_filter = ['subject__parent_subcategory__parent_category', 'is_published', 'is_free']
    search_fields = ['name', 'author__id', 'author__first_name', 'author__last_name']

    def author_id(self, obj):
        return obj.author.id

    def bname(self, obj):
        return format_html('<b>{}</b>', obj.name)

    def author_fullname_link(self, obj):
        full_name = get_user_full_name(obj.author)
        url = reverse('admin:courses_course_changelist') + '?' + urlencode({'author__id': obj.author.id})
        return format_html('<a href="{}">{}</a>', url, full_name)

    def show_students_link(self, obj):
        count = obj.num_students()
        url = reverse('admin:auth_user_changelist') + '?' + urlencode({'student_courses__id': obj.id})
        return format_html('<a href="{}">{} students</a>', url, count)

    bname.short_description = 'Name'
    show_students_link.short_description = 'Number of students'
    author_fullname_link.short_description = 'Author'

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'course_name_link', 'course_author_fullname_link']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'course__name']

    def course_name_link(self, obj):
        name = obj.course.name
        url = reverse('admin:courses_section_changelist') + '?' + urlencode({'course__id': obj.course.id})
        return format_html('<a href="{}">{}</a>', url, name)
    
    def course_author_fullname_link(self, obj):
        fullname = get_user_full_name(obj.course.author)
        url = reverse('admin:auth_user_change', kwargs={'object_id': obj.course.author.id})
        return format_html('<a href="{}">{}</a>', url, fullname)
    

    course_name_link.short_description = 'Course name'
    course_author_fullname_link.short_description = 'Course author'

@admin.register(StripeCourse)
class StripeCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_name', 'course_author_link']
    search_fields = ['course__name', 'course__author__first_name', 'course__author__last_name']

    def course_name(self, obj):
        return obj.course.name
    
    def course_author_link(self, obj):
        fullname = get_user_full_name(obj.course.author)
        url = reverse('admin:auth_user_change', kwargs={'object_id': obj.course.author.id})
        return format_html('<a href="{}">{}</a>', url, fullname)

    course_author_link.short_description = 'Course author'

@admin.register(CoursePayment)
class CoursePaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_name_link', 'student_name_link' ,'status', 'option']
    list_display_links = ['id', 'course_name_link']
    list_filter = ['status']
    search_fields = ['id', 'student__first_name', 'student__last_name']

    def course_name_link(self, obj):
        return obj.course.name

    def student_name_link(self, obj):
        fullname = get_user_full_name(obj.student)
        url = reverse('admin:auth_user_change', kwargs={'object_id': obj.student.id})
        return format_html('<a href="{}">{}</a>', url, fullname)
    
    course_name_link.short_description = 'Course'
    student_name_link.short_description = 'Student'


admin.site.register(CoursePrice)
admin.site.register(CourseUpgradePrice)