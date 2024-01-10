from rest_framework import routers
from .api.views import CourseViewSet, SectionViewSet, LessonViewSet, AdditionalFileViewSet, GetUser
from .api.views import TestViewSet, TestQuestionViewSet, HomeworkViewSet, CourseSearchView, TestCompletionView, CourseStatisticsView
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
    path('courses/search/', CourseSearchView.as_view(), name='course-search'),
    path('courses/by_subject/<int:id>/statistics/', CourseStatisticsView.as_view(), name='course-statistics'),
    path('test-completions/', TestCompletionView.as_view(), name='test-completion'),
]
urlpatterns += router.urls