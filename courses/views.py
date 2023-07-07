from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets
from .models import Course, Section, Lesson, AdditionalFile, Test, TestQuestion, Homework
from .serializers import CourseSerializer, SectionSerializer, LessonSerializer, AdditionalFileSerializer, HomeworkSerializer
from .serializers import TestSerializer, TestQuestionSerializer, CoursePaymentSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
import stripe
from decouple import config

stripe.api_key = config('STRIPE_KEY')


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication]

    @action(methods=['get'], detail=True)
    def buy(self, request, pk=None):
        course = Course.objects.get(id=pk)
        line_items = CoursePaymentSerializer(course).data
        session = stripe.checkout.Session.create(
            success_url=request.build_absolute_uri(reverse('course-single', kwargs={'id': pk})),
            client_reference_id=request.user.id,
            line_items=[line_items],
            currency='rub',
            mode="payment",
        )
        return Response({'id': session['id']})


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class AdditionalFileViewSet(viewsets.ModelViewSet):
    queryset = AdditionalFile.objects.all()
    serializer_class = AdditionalFileSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TestQuestionViewSet(viewsets.ModelViewSet):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    

class GetUser(APIView):
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })

# Create your views here.
