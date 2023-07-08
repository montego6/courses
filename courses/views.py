from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets
from .models import Course, Section, Lesson, AdditionalFile, Test, TestQuestion, Homework
from .serializers import CourseSerializer, SectionSerializer, LessonSerializer, AdditionalFileSerializer, HomeworkSerializer
from .serializers import TestSerializer, TestQuestionSerializer, CourseItemPaymentSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
import stripe
from decouple import config

stripe.api_key = config('STRIPE_KEY')

# (?P<course_pk>[^/.]+)/
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication]

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
    
    # @action(methods=['get'], detail=True)
    # def is_paid(self, request, pk=None):
    #     course = Course.objects.get(id=pk)


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
