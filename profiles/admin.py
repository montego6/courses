from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from profiles.models import TeacherProfile
from users.helpers import get_user_full_name

# Register your models here.

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user_link', 'balance']
    search_fields = ['user__first_name', 'user__last_name']

    def full_name(self, obj):
        return get_user_full_name(obj.user)
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', kwargs={'object_id': obj.user.id})
        return format_html('<a href="{}">{}</a>', url, obj.user)
    


admin.site.register(TeacherProfile, TeacherProfileAdmin)