from django.urls import path
from rest_framework import routers
from .api.views import CategoryStatisticsView, CategoryViewSet, SubCategoryStatisticsView, SubCategoryViewSet, SubjectStatisticsView, SubjectViewSet

router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'subjects', SubjectViewSet)
urlpatterns = [
    path('categories/statistics/', CategoryStatisticsView.as_view(), name='api-categories-statistics'),
    path('subcategories/by_category/<int:id>/statistics/', SubCategoryStatisticsView.as_view(), name='api-subcategories-statistics'),
    path('subjects/by_subcategory/<int:id>/statistics/', SubjectStatisticsView.as_view(), name='api-subjects-statistics'),
]
urlpatterns += router.urls