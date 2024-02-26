from django.urls import path

from profiles.views import MyCoursesView, MyProfileView, TeacherProfileView


urlpatterns = [path('myprofile/', MyProfileView.as_view(), name='my'),
               path('teacher/<int:id>/', TeacherProfileView.as_view(), name='teacher'),
               path('mycourses/', MyCoursesView.as_view(), name='my-courses')
            ]
