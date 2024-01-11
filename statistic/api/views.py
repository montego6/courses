from rest_framework import generics
from categories.models import Category, SubCategory, Subject
from courses.models import Course
from .serializers import CategoryStatisticsSerializer, CourseStatisticsSerializer, SubCategoryStatisticsSerializer, SubjectStatisticsSerializer


class CategoryStatisticsView(generics.ListAPIView):
    queryset = Category.statistics.all()
    serializer_class = CategoryStatisticsSerializer


class SubCategoryStatisticsView(generics.ListAPIView):
    serializer_class = SubCategoryStatisticsSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('id')
        return SubCategory.statistics.by_category(category_id=category_id)
    

class SubjectStatisticsView(generics.ListAPIView):
    serializer_class = SubjectStatisticsSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs.get('id')
        return Subject.statistics.by_subcategory(subcategory_id=subcategory_id)


class CourseStatisticsView(generics.ListAPIView):
    serializer_class = CourseStatisticsSerializer

    def get_queryset(self):
        subject_id = self.kwargs.get('id')
        return Course.statistics.by_subject(subject_id=subject_id)