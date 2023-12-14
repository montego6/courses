from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Category, SubCategory, Subject
from .serializers import CategorySerializer, CategoryStatisticsSerializer, SubCategorySerializer, SubCategoryStatisticsSerializer, SubjectSerializer, SubjectStatisticsSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


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