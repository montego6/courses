from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Category, SubCategory, Subject
from .serializers import CategorySerializer, CategoryStatisticsSerializer, SubCategorySerializer, SubjectSerializer

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