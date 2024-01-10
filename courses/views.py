from django.contrib.auth import get_user_model
from courses.blogic_stripe import StripeSession
from .models import Course, Section, CoursePayment
from reviews.models import Review
from .serializers import CourseSerializer, CourseStatisticsSerializer, SectionSerializer
from .serializers import CourseSearchSerializer
from . import consts
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import status




User = get_user_model()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(methods=['get'], detail=True, url_path=r'buy/(?P<option>[^/.]+)')
    def buy(self, request, option, pk=None):
        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response({'detail': 'course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            stripe_session = StripeSession(course, option)
            session = stripe_session.buy(request)
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

    



class CourseSearchView(generics.ListAPIView):
    serializer_class = CourseSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query')
        queryset = Course.custom_objects.search_by_query(query)
        return queryset
    


class CourseStatisticsView(generics.ListAPIView):
    serializer_class = CourseStatisticsSerializer

    def get_queryset(self):
        subject_id = self.kwargs.get('id')
        return Course.statistics.by_subject(subject_id=subject_id)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class GetUser(APIView):
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })

# Create your views here.
