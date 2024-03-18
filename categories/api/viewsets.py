from rest_framework import viewsets
from core.permissions import IsAdminForPOST
from categories.models import Category, SubCategory, Subject
from .serializers import CategorySerializer, SubCategorySerializer, SubjectSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related('subcategories').prefetch_related('subcategories__subjects')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminForPOST]


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminForPOST]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminForPOST]