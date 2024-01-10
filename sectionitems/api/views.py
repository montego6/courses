from rest_framework import generics
from courses.api.serializers import TestCompletionSerializer

from sectionitems.models import TestCompletion

class TestCompletionView(generics.CreateAPIView):
    queryset = TestCompletion.objects.all()
    serializer_class = TestCompletionSerializer