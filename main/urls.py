from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('mycourses/create/', views.CourseCreateView.as_view(), name='add'),
    path('mycourses/<int:id>/', views.CourseContentView.as_view(), name='content'),
    path('course/<int:id>/', views.CourseDetailView.as_view(), name='single'),
    path('search', views.CourseSearchView.as_view(), name='search'),
    path('webhook/', views.my_webhook_view),
]
