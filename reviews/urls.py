from django.urls import path
from .views import ReviewCreateView, ReviewListView

urlpatterns = [
    path('reviews/', ReviewCreateView.as_view(), name='reviews-create'),
    path('reviews/<int:pk>/', ReviewListView.as_view(), name='reviews-list'),
]