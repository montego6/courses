from django.urls import path
from rest_framework import routers
from categories.api.viewsets import CategoryViewSet, SubCategoryViewSet, SubjectViewSet
from courses.api.views import CoursePriceDeleteView, CourseSearchView, CoursePriceCreateView
from courses.api.viewsets import CourseViewSet, SectionViewSet
from profiles.api.views import HasTeacherProfile
from profiles.api.viewsets import TeacherProfileViewSet
from reviews.api.views import ReviewCreateView
from sectionitems.api.views import TestCompletionView
from sectionitems.api.viewsets import AdditionalFileViewSet, HomeworkViewSet, LessonViewSet, TestQuestionViewSet, TestViewSet
from statistic.api.views import CategoryStatisticsView, CourseStatisticsView, SubCategoryStatisticsView, SubjectStatisticsView

urlpatterns = []

categories_router = routers.SimpleRouter()
categories_router.register(r'categories', CategoryViewSet)
categories_router.register(r'subcategories', SubCategoryViewSet)
categories_router.register(r'subjects', SubjectViewSet)

urlpatterns += [
    path('categories/statistics/', CategoryStatisticsView.as_view(), name='categories-statistics'),
    path('subcategories/by_category/<int:id>/statistics/', SubCategoryStatisticsView.as_view(), name='subcategories-statistics'),
    path('subjects/by_subcategory/<int:id>/statistics/', SubjectStatisticsView.as_view(), name='subjects-statistics'),
    path('courses/by_subject/<int:id>/statistics/', CourseStatisticsView.as_view(), name='course-statistics'),
]
urlpatterns += categories_router.urls

courses_router = routers.SimpleRouter()
courses_router.register(r'courses', CourseViewSet)
courses_router.register(r'sections', SectionViewSet)

urlpatterns += [
    path('courses/search/', CourseSearchView.as_view(), name='course-search'),
    path('courses/prices/', CoursePriceCreateView.as_view(), name='course-price-add'),
    path('courses/prices/<int:pk>', CoursePriceDeleteView.as_view(), name='course-price-delete'),
]

urlpatterns += courses_router.urls


profiles_router = routers.SimpleRouter()
profiles_router.register(r'profiles', TeacherProfileViewSet)

urlpatterns += [
    path('profiles/has_profile/', HasTeacherProfile.as_view(), name='has-teacher-profile'),
]

urlpatterns += profiles_router.urls


urlpatterns += [
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
]


items_router = routers.SimpleRouter()
items_router.register(r'lessons', LessonViewSet)
items_router.register(r'extra_files', AdditionalFileViewSet)
items_router.register(r'tests', TestViewSet)
items_router.register(r'questions', TestQuestionViewSet)
items_router.register(r'homeworks', HomeworkViewSet)

urlpatterns += [
    path('test-completions/', TestCompletionView.as_view(), name='test-completion'),
]

urlpatterns += items_router.urls