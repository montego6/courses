from django.contrib.auth import get_user_model
from ..models import Course
from .serializers import CourseStatisticsSerializer
from .serializers import CourseSearchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics


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
