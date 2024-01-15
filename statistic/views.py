
from django.views.generic import TemplateView


class CategoryStatisticsView(TemplateView):
    template_name = 'statistic-main.html'


class SubCategoryStatisticsView(TemplateView):
    template_name = 'statistic-subcategories.html'


class SubjectStatisticsView(TemplateView):
    template_name = 'statistic-subjects.html'


class CourseBySubjectStatisticsView(TemplateView):
    template_name = 'statistic-courses.html'