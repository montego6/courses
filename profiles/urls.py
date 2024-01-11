from django.urls import path
from django.views.generic.base import TemplateView




urlpatterns = [path('myprofile/', TemplateView.as_view(template_name='my-profile.html'), name='my-profile'),
               path('teacher/<int:id>', TemplateView.as_view(template_name='teacher-page.html'), name='teacher-page'),
               
            ]
