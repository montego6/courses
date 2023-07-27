from rest_framework import routers
from .views import CourseViewSet, SectionViewSet, LessonViewSet, AdditionalFileViewSet, GetUser
from .views import TestViewSet, TestQuestionViewSet, HomeworkViewSet, CourseSearchView
from django.urls import path

router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'extra_files', AdditionalFileViewSet)
router.register(r'tests', TestViewSet)
router.register(r'questions', TestQuestionViewSet)
router.register(r'homeworks', HomeworkViewSet)
urlpatterns = [
    path('user/', GetUser.as_view()),
    path('courses/search/', CourseSearchView.as_view())
]
urlpatterns += router.urls