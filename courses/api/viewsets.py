from django.db.models import Subquery
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core import consts

from courses.blogic_stripe import StripeSession, create_stripe_upgrade_prices
from reviews.models import Review
from .serializers import CourseSearchSerializer, CourseSerializer, SectionSerializer

from courses.models import Course, CoursePayment, CoursePrice, CourseUpgradePrice, Section


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'

    @action(methods=['get'], detail=False, url_path=r'by_subject/(?P<subject_id>[^/.]+)')
    def courses_by_subject(self, request, subject_id):
        courses = Course.objects.filter(subject_id=subject_id)
        data = CourseSearchSerializer(courses, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False, url_path=r'by_subcategory/(?P<subcategory_id>[^/.]+)')
    def courses_by_subcategory(self, request, subcategory_id):
        courses = Course.objects.filter(subject__parent_subcategory__id=subcategory_id)
        data = CourseSearchSerializer(courses, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False, url_path=r'by_category/(?P<category_id>[^/.]+)')
    def courses_by_category(self, request, category_id):
        courses = Course.objects.filter(subject__parent_subcategory__parent_category__id=category_id)
        data = CourseSearchSerializer(courses, many=True).data
        return Response(data, status=status.HTTP_200_OK)

  
    @action(methods=['get'], detail=True, url_path='publish')
    def publish(self, request, slug=None):
        course = Course.objects.get(slug=slug)
        create_stripe_upgrade_prices(course)
        course.is_published = True
        course.save()
        return Response({'detail': 'course is published'}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path=r'buy/(?P<option>[^/.]+)')
    def buy(self, request, option, slug=None):
        try:
            course = Course.objects.get(slug=slug)
        except Course.DoesNotExist:
            return Response({'detail': 'course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                price_obj = CoursePrice.objects.get(course=course, option=option)
            except CoursePrice.DoesNotExist:
                return Response({'detail': 'price for this course and option does not exist'}, status=status.HTTP_404_NOT_FOUND)
            else:
                session = StripeSession(course, option).buy(request, price_obj)
                return Response({'id': session['id']})
    
    @action(methods=['get'], detail=True, url_path=r'upgrade/(?P<option>[^/.]+)')
    def upgrade(self, request, option, slug=None):
        try:
            course = Course.objects.get(slug=slug)
        except Course.DoesNotExist:
            return Response({'detail': 'course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                paid_option = CoursePayment.objects.get(course=course, student=request.user).option
            except CoursePayment.DoesNotExist:
                return Response({'detail': 'course payment does not exist'}, status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    upgrade_obj = CourseUpgradePrice.objects.get(course=course, upgrade_from=paid_option, upgrade_to=option)
                except CourseUpgradePrice.DoesNotExist:
                    return Response({'detail': 'upgrade for this course and option does not exist'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    session = StripeSession(course, option, paid_option).upgrade(request, upgrade_obj)
                    return Response({'id': session['id']})
    

    @action(methods=['get'], detail=False, url_path=r'barsearch/(?P<query>[^/.]+)')
    def bar_search(self, request, query):
        courses = Course.custom_objects.search_by_query(query)
        serializer = CourseSearchSerializer(courses, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True)
    def payment_info(self, request, slug=None):
        user = request.user
        if not user.is_authenticated:
            return Response({'payment': consts.COURSE_PAYMENT_NOT_PAID, 'option': consts.COURSE_OPTION_FREE}, status=status.HTTP_200_OK)
        try:
            payment = CoursePayment.objects.get(course__slug=slug, student=user)
        except CoursePayment.DoesNotExist:
            return Response({'payment': consts.COURSE_PAYMENT_NOT_PAID, 'option': consts.COURSE_OPTION_FREE}, status=status.HTTP_200_OK)
        else:
            return Response({'payment': consts.COURSE_PAYMENT_PAID, 'option': payment.option}, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True)
    def review_info(self, request, slug=None):
        user = request.user
        if user.is_authenticated and Review.objects.filter(student=user, course__slug=slug).exists():
            return Response({'review': True})
        return Response({'review': False})
    
    @action(methods=['get'], detail=False)
    def my_courses(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'user should be logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        paid_courses_subq = CoursePayment.objects.filter(student=user, status=consts.COURSE_PAYMENT_PAID).values('course')
        my_courses = Course.objects.filter(id__in=Subquery(paid_courses_subq))
        serializer = CourseSearchSerializer(my_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    
