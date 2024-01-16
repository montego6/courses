from django.urls import path

from profiles.views import MyProfileView, TeacherProfileView


urlpatterns = [path('myprofile/', MyProfileView.as_view(), name='my'),
               path('teacher/<int:id>', TeacherProfileView.as_view(), name='teacher'),
            ]
