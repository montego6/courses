from .api.views import CourseSearchView
from django.urls import path

urlpatterns = [
    path('courses/search/', CourseSearchView.as_view(), name='course-search'),
]