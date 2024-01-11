from django.urls import path, include
from django.views.generic.base import TemplateView
from rest_framework import routers
from .api.views import HasTeacherProfile, TeacherProfileViewSet



urlpatterns = [path('myprofile/', TemplateView.as_view(template_name='my-profile.html'), name='my-profile'),
               path('teacher/<int:id>', TemplateView.as_view(template_name='teacher-page.html'), name='teacher-page'),
               
            ]
