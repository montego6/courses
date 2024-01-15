from django.urls import path
from profiles.models import TeacherProfile

from profiles.views import MyProfileView


urlpatterns = [path('myprofile/', MyProfileView.as_view(), name='my'),
               path('teacher/<int:id>', TeacherProfile.as_view(), name='teacher'),
            ]
