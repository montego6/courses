from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import get_user_model

from courses.blogic import StripeSession
from .models import Course, Section, Lesson, AdditionalFile, Test, TestQuestion, Homework, CoursePayment
from .models import TestCompletion
from reviews.models import Review
from .serializers import CourseSerializer, SectionSerializer, LessonSerializer, AdditionalFileSerializer, HomeworkSerializer
from .serializers import TestSerializer, TestQuestionSerializer, CourseItemPaymentSerializer, CourseSearchSerializer
from .serializers import TestCompletionSerializer
from . import consts
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import status

import stripe
from decouple import config

stripe.api_key = config('STRIPE_KEY')

User = get_user_model()

# (?P<course_pk>[^/.]+)/
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # authentication_classes = [SessionAuthentication]

    @action(methods=['get'], detail=True, url_path=r'buy/(?P<option>[^/.]+)')
    def buy(self, request, option, pk=None):
        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response({'detail': 'course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            stripe_session = StripeSession(course, option)
            session = stripe_session.buy(request)
        # price = course.stripe.price if not option else course.stripe.option_prices[option]
        # line_items = {'price': price, 'quantity': 1}
        # # line_items = CourseItemPaymentSerializer(course).data
        # metadata = {'option': option} if option else {'option': consts.COURSE_OPTION_BASIC}
        # session = stripe.checkout.Session.create(
        #     success_url=request.build_absolute_uri(reverse('course-single', kwargs={'id': pk})),
        #     client_reference_id=request.user.id,
        #     line_items=[line_items],
        #     currency='rub',
        #     mode="payment",
        #     metadata=metadata
        # )
            return Response({'id': session['id']})
    
    @action(methods=['get'], detail=True, url_path=r'upgrade/(?P<option>[^/.]+)')
    def upgrade(self, request, option, pk=None):
        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response({'detail': 'course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                paid_option = CoursePayment.objects.get(course=course, student=request.user).option
            except CoursePayment.DoesNotExist:
                return Response({'detail': 'course payment does not exist'}, status=status.HTTP_404_NOT_FOUND)
            else:
                stripe_session = StripeSession(course, option, paid_option)
                session = stripe_session.upgrade(request)
        # price = course.stripe.option_prices[option]['upgrade'][paid_option]
        # line_items = {'price': price, 'quantity': 1}
        # metadata = {'option': option, 'upgrade': True, 'course': course.id} 
        # session = stripe.checkout.Session.create(
        #     success_url=request.build_absolute_uri(reverse('course-single', kwargs={'id': pk})),
        #     client_reference_id=request.user.id,
        #     line_items=[line_items],
        #     currency='rub',
        #     mode="payment",
        #     metadata=metadata
        # )
                return Response({'id': session['id']})
    

    @action(methods=['get'], detail=False, url_path=r'barsearch/(?P<query>[^/.]+)')
    def bar_search(self, request, query):
        courses = Course.custom_objects.search_by_query(query)
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True)
    def payment_info(self, request, pk=None):
        user = request.user
        if not isinstance(user, User):
            return Response({'payment': consts.COURSE_PAYMENT_NOT_PAID, 'option': consts.COURSE_OPTION_FREE}, status=status.HTTP_200_OK)
        try:
            payment = CoursePayment.objects.get(course_id=pk, student=user)
        except CoursePayment.DoesNotExist:
            return Response({'payment': consts.COURSE_PAYMENT_NOT_PAID, 'option': consts.COURSE_OPTION_FREE}, status=status.HTTP_200_OK)
        else:
            return Response({'payment': consts.COURSE_PAYMENT_PAID, 'option': payment.option}, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True)
    def review_info(self, request, pk=None):
        user = request.user
        if user.is_authenticated and Review.objects.filter(student=user, course__id=pk).exists():
            return Response({'review': True})
        return Response({'review': False})

    
    # @action(methods=['get'], detail=True)
    # def is_paid(self, request, pk=None):
    #     course = Course.objects.get(id=pk)


class CourseSearchView(generics.ListAPIView):
    serializer_class = CourseSearchSerializer

    def get_queryset(self):
        # queryset = Course.objects.all()
        query = self.request.query_params.get('query')
        # queryset = queryset.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(full_description__icontains=query))
        queryset = Course.custom_objects.search_by_query(query)
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


class TestCompletionView(generics.CreateAPIView):
    queryset = TestCompletion.objects.all()
    serializer_class = TestCompletionSerializer

    

class GetUser(APIView):
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })

# Create your views here.
