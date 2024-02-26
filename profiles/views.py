from django.views.generic import TemplateView


class MyProfileView(TemplateView):
    template_name = 'my-profile.html'


class TeacherProfileView(TemplateView):
    template_name = 'teacher-page.html'


class MyCoursesView(TemplateView):
    template_name = 'my-courses.html'