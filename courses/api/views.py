from django.contrib.auth import get_user_model

from courses.blogic_stripe import create_stripe_upgrade_prices
from ..models import Course, CoursePrice
from .serializers import CoursePriceSerializer, CourseSearchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status


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


class CoursePublishView(APIView):
    def get(self, request):
        id = self.kwargs.get('id')
        course = Course.objects.get(id=id)
        create_stripe_upgrade_prices(course)
        course.is_published = True
        course.save()
        return Response({'detail': 'course is published'}, status=status.HTTP_200_OK)
