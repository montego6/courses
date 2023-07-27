from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from rest_framework import viewsets
from .models import Course, Section, Lesson, AdditionalFile, Test, TestQuestion, Homework
from .serializers import CourseSerializer, SectionSerializer, LessonSerializer, AdditionalFileSerializer, HomeworkSerializer
from .serializers import TestSerializer, TestQuestionSerializer, CourseItemPaymentSerializer, CourseSearchSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics

import stripe
from decouple import config

stripe.api_key = config('STRIPE_KEY')

# (?P<course_pk>[^/.]+)/
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # authentication_classes = [SessionAuthentication]

    @action(methods=['get'], detail=True, url_path=r'buy/(?P<option>[^/.]+)')
    def buy(self, request, option, pk=None):
        course = Course.objects.get(id=pk)
        price = course.stripe.price if not option else course.stripe.option_prices[option]
        line_items = {'price': price, 'quantity': 1}
        # line_items = CourseItemPaymentSerializer(course).data
        metadata = {'option': option} if option else {'option': 'basic'}
        session = stripe.checkout.Session.create(
            success_url=request.build_absolute_uri(reverse('course-single', kwargs={'id': pk})),
            client_reference_id=request.user.id,
            line_items=[line_items],
            currency='rub',
            mode="payment",
            metadata=metadata
        )
        return Response({'id': session['id']})
    

    @action(methods=['get'], detail=False, url_path=r'barsearch/(?P<query>[^/.]+)')
    def bar_search(self, request, query):
        courses = Course.objects.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(full_description__icontains=query))
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data)
    
    # @action(methods=['get'], detail=True)
    # def is_paid(self, request, pk=None):
    #     course = Course.objects.get(id=pk)


class CourseSearchView(generics.ListAPIView):
    serializer_class = CourseSearchSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        query = self.request.query_params.get('query')
        queryset = queryset.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(full_description__icontains=query))
        return queryset


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
