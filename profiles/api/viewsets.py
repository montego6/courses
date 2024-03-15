from rest_framework.viewsets import ModelViewSet
from core.permissions import IsProfileOwner
from profiles.models import TeacherProfile

from .serializers import TeacherProfileSerializer


class TeacherProfileViewSet(ModelViewSet):
    serializer_class = TeacherProfileSerializer
    queryset = TeacherProfile.objects.all()
    permission_classes = [IsProfileOwner]