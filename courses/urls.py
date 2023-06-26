from rest_framework import routers
from .views import CourseViewSet, SectionViewSet, LessonViewSet, AdditionalFileViewSet, GetUser
from .views import TestViewSet, TestQuestionViewSet
from django.urls import path

router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'extra_files', AdditionalFileViewSet)
router.register(r'tests', TestViewSet)
router.register(r'questions', TestQuestionViewSet)
urlpatterns = router.urls + [path('user/', GetUser.as_view())]