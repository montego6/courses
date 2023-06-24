from rest_framework import routers
from .views import CourseViewSet, SectionViewSet, LessonViewSet, GetUser
from django.urls import path

router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'lessons', LessonViewSet)
urlpatterns = router.urls + [path('user/', GetUser.as_view())]