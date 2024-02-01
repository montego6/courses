from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from courses.models import Course
from ..models import Review
from .serializers import ReviewSerializer


class ReviewCreateView(generics.GenericAPIView, CreateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request):
        course_slug = request.data.get('course_slug')
        course = Course.objects.get(slug=course_slug)
        data = {
            'comment': request.data.get('comment'),
            'rating': request.data.get('rating'),
            'course': course.id,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class ReviewListView(generics.ListAPIView):
#     serializer_class = ReviewSerializer

#     def get_queryset(self):
#         course = self.kwargs.get('pk')
#         return Review.objects.filter(course=course)