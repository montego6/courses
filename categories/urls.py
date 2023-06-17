from rest_framework import routers
from .views import CategoryViewSet, SubCategoryViewSet, SubjectViewSet

router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'subjects', SubjectViewSet)
urlpatterns = router.urls