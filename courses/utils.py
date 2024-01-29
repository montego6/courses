from core import consts
from courses.models import CoursePayment


def get_user_from_context(context):
    user = None
    request = context.get('request')
    if request and hasattr(request, 'user'):
        if request.user.is_authenticated:
            user = request.user
    return user
    

def make_payment_context(course, student):
    context = {}
    try:
        payment = CoursePayment.objects.get(course=course, student=student, status=consts.COURSE_PAYMENT_PAID)
    except CoursePayment.DoesNotExist:
        context['payment'] = consts.COURSE_OPTION_FREE
    else:
        context['payment'] = payment.option
    return context

    

class ExtraContext:
    def __init__(self, context, user, course) -> None:
        self.context = context
        self.user = user
        self.course = course

    def is_author(self):
        return self.user == self.course.author
    
    def update_context(self):
        self.context['is_author'] = self.is_author()
        self.context['user'] = self.user
        return self.context
    

