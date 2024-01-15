from django.urls import path
from statistic.views import CategoryStatisticsView, CourseBySubjectStatisticsView, SubCategoryStatisticsView, SubjectStatisticsView


urlpatterns = [
    path('main/', CategoryStatisticsView.as_view(), name='main'),
    path('subcategories/by_category/<int:id>/', SubCategoryStatisticsView.as_view(), name='subcategories'),
    path('subjects/by_subcategory/<int:id>/', SubjectStatisticsView.as_view(), name='subjects'),
    path('courses/by_subject/<int:id>/', CourseBySubjectStatisticsView.as_view(), name='courses'),
]