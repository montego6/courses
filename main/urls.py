from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('mycourses/create/', views.CourseCreateView.as_view(), name='course-add'),
    path('mycourses/<int:id>/', views.CourseContentView.as_view(), name='course-content'),
    path('course/<int:id>/', views.CourseDetailView.as_view(), name='course-single'),
    path('search', views.CourseSearchView.as_view(), name='course-search'),
    path('webhook/', views.my_webhook_view),
]
