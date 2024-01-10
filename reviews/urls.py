from django.urls import path
from .api.views import ReviewCreateView, ReviewListView

urlpatterns = [
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/', ReviewListView.as_view(), name='review-list'),
]