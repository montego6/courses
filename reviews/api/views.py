from rest_framework import generics
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from ..models import Review
from .serializers import ReviewSerializer


class ReviewCreateView(generics.GenericAPIView, CreateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request):
        # request.data.update(student=self.request.user.id)
        return self.create(request)


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        course = self.kwargs.get('pk')
        return Review.objects.filter(course=course)