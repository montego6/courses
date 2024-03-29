from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('courses/by_subject/<int:subject_id>/', views.CoursesBySubject.as_view(), name='by-subject'),
    path('courses/by_subcategory/<int:subcategory_id>/', views.CoursesBySubcategory.as_view(), name='by-subcategory'),
    path('courses/by_category/<int:category_id>/', views.CoursesByCategory.as_view(), name='by-category'),
    path('mycourses/create/', views.CourseCreateView.as_view(), name='add'),
    path('mycourses/<int:id>/preview/', views.CoursePreviewView.as_view(), name='preview'),
    path('mycourses/<slug:slug>/', views.CourseContentView.as_view(), name='content'),
    path('mycourses/<slug:slug>/edit/', views.CourseEditView.as_view(), name='edit'),
    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='single'),
    path('search', views.CourseSearchView.as_view(), name='search'),
    path('webhook/', views.my_webhook_view),
]
