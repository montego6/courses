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
        return self.create(request)
