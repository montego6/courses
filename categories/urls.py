from django.urls import path
from rest_framework import routers
from .views import CategoryStatisticsView, CategoryViewSet, SubCategoryViewSet, SubjectViewSet

router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'subjects', SubjectViewSet)
urlpatterns = [
    path('categories/statistics/', CategoryStatisticsView.as_view(), name='api-categories-statistics')
]
urlpatterns += router.urls