from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from .models import Category, SubCategory, Subject
# Register your models here.

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category_link']

    def parent_category_link(self, obj):
        url = reverse('admin:categories_subcategory_changelist') + '?' + urlencode({'parent_category__id': obj.parent_category.id})
        return format_html('<a href="{}">{}</a>', url, obj.parent_category.name)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_subcategory_link']

    def parent_subcategory_link(self, obj):
        url = reverse('admin:categories_subject_changelist') + '?' + urlencode({'parent_subcategory__id': obj.parent_subcategory.id})
        return format_html('<a href="{}">{}</a>', url, obj.parent_subcategory.name)

admin.site.register(Category)
# admin.site.register(SubCategory)
# admin.site.register(Subject)