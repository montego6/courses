from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path('main/', TemplateView.as_view(template_name='statistic-main.html'), name='statistic-main'),
    path('subcategories/by_category/<int:id>', TemplateView.as_view(template_name='statistic-subcategories.html'), name='statistic-subcategories'),
]