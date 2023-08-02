from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import TeacherProfile
from .serializers import TeacherProfileSerializer


class HasTeacherProfile(APIView):
    def get(self, request):
        teacher_profile = TeacherProfile.objects.filter(user=request.user)
        if teacher_profile.exists():
            serializer = TeacherProfileSerializer(teacher_profile[0])
            return Response({'profile': True, 'content': serializer.data})
        else:
            return Response({'profile': False})


class TeacherProfileViewSet(ModelViewSet):
    serializer_class = TeacherProfileSerializer
    queryset = TeacherProfile.objects.all()
# Create your views here.
