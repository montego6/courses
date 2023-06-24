from django.shortcuts import render
from rest_framework import viewsets
from .models import Course, Section, Lesson
from .serializers import CourseSerializer, SectionSerializer, LessonSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class GetUser(APIView):
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })

# Create your views here.
