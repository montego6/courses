from django.urls import path
from main import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('course/create/', TemplateView.as_view(template_name='course-add.html'), name='course-add'),
    path('course/<int:id>', TemplateView.as_view(template_name='course-single.html'), name='course-single'),
]
