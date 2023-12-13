from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path('main/', TemplateView.as_view(template_name='statistic-main.html'), name='statistic-main'),
]