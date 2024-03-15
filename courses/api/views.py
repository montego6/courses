from django.contrib.auth import get_user_model

from ..models import Course, CoursePrice
from .serializers import CoursePriceSerializer, CourseSearchSerializer
from rest_framework import generics


User = get_user_model()


class CourseSearchView(generics.ListAPIView):
    serializer_class = CourseSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query')
        queryset = Course.custom_objects.search_by_query(query)
        return queryset



class CoursePriceCreateView(generics.CreateAPIView):
    queryset = CoursePrice.objects.all()
    serializer_class = CoursePriceSerializer


class CoursePriceDeleteView(generics.UpdateAPIView):
    queryset = CoursePrice.objects.all()
    serializer_class = CoursePriceSerializer



