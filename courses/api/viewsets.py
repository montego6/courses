from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core import consts

from courses.blogic_stripe import StripeSession
from reviews.models import Review
from .serializers import CourseSerializer, SectionSerializer

from courses.models import Course, CoursePayment, CoursePrice, CourseUpgradePrice, Section


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'

    @action(methods=['get'], detail=True, url_path=r'buy/(?P<option>[^/.]+)')
    def buy(self, request, option, pk=None):
        try:
            course = Course.objects.get(id=pk)
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
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True)
    def payment_info(self, request, pk=None):
        user = request.user
        if not user.is_authenticated:
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
    

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer