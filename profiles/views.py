from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import TeacherProfile
from .serializers import TeacherProfileSerializer
from courses.models import Course
from courses.serializers import CourseProfileSerializer


class HasTeacherProfile(APIView):
    def get(self, request):
        teacher_profile = TeacherProfile.objects.filter(user=request.user)
        if teacher_profile.exists():
            serializer = TeacherProfileSerializer(teacher_profile[0])
            courses = Course.objects.filter(author=request.user)
            courses_data = CourseProfileSerializer(courses, many=True).data
            return Response({'profile': True, 'content': serializer.data, 'courses': courses_data})
        else:
            return Response({'profile': False})


class TeacherProfileViewSet(ModelViewSet):
    serializer_class = TeacherProfileSerializer
    queryset = TeacherProfile.objects.all()
# Create your views here.
