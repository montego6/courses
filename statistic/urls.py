from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path('main/', TemplateView.as_view(template_name='statistic-main.html'), name='statistic-main'),
    path('subcategories/by_category/<int:id>/', TemplateView.as_view(template_name='statistic-subcategories.html'), name='statistic-subcategories'),
    path('subjects/by_subcategory/<int:id>/', TemplateView.as_view(template_name='statistic-subjects.html'), name='statistic-subjects'),
    path('courses/by_subject/<int:id>/', TemplateView.as_view(template_name='statistic-courses.html'), name='statistic-courses'),
]