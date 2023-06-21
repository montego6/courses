from django.shortcuts import render
from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication]

class GetUser(APIView):
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })

# Create your views here.
