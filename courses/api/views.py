from django.contrib.auth import get_user_model
from courses.blogic_stripe import StripeSession
from ..models import Course, Section, CoursePayment
from reviews.models import Review
from .serializers import CourseSerializer, CourseStatisticsSerializer, SectionSerializer
from .serializers import CourseSearchSerializer
from ...core import consts
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import status


User = get_user_model()


class CourseSearchView(generics.ListAPIView):
    serializer_class = CourseSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query')
        queryset = Course.custom_objects.search_by_query(query)
        return queryset


class CourseStatisticsView(generics.ListAPIView):
    serializer_class = CourseStatisticsSerializer

    def get_queryset(self):
        subject_id = self.kwargs.get('id')
        return Course.statistics.by_subject(subject_id=subject_id)





class GetUser(APIView):
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })

# Create your views here.
