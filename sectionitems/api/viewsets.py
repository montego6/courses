from rest_framework import viewsets

from core.permissions import IsSectionItemOwner
from .serializers import AdditionalFileSerializer, HomeworkSerializer, LessonSerializer, TestQuestionSerializer, TestSerializer
from sectionitems.models import AdditionalFile, Homework, Lesson, Test, TestQuestion


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsSectionItemOwner]


class AdditionalFileViewSet(viewsets.ModelViewSet):
    queryset = AdditionalFile.objects.all()
    serializer_class = AdditionalFileSerializer
    permission_classes = [IsSectionItemOwner]


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsSectionItemOwner]


class TestQuestionViewSet(viewsets.ModelViewSet):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer
    permission_classes = [IsSectionItemOwner]


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsSectionItemOwner]