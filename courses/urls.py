from rest_framework import routers
from .views import CourseViewSet, GetUser
from django.urls import path

router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet)
urlpatterns = router.urls + [path('user/', GetUser.as_view())]