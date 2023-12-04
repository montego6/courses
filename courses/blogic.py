from courses import consts
from courses.models import CoursePayment, TestCompletion


def get_user_from_context(context):
    user = None
    request = context.get('request')
    if request and hasattr(request, 'user'):
        if request.user.is_authenticated:
            user = request.user
    return user
    

# class GetUserFromContext:
#     def __init__(self, context) -> None:
#         self.context = context
#         self.user = None

#     def get_user(self):
#         request = self.context.get('request')
#         if request and hasattr(request, 'user'):
#             if request.user.is_authenticated:
#                 self.user = request.user
#         return self.user
    
def make_payment_context(course, student):
    context = {}
    try:
        payment = CoursePayment.objects.get(course=course, student=student)
    except CoursePayment.DoesNotExist:
        context['payment'] = consts.COURSE_OPTION_FREE
    else:
        context['payment'] = payment.option
    return context

# class MakePaymentContext:
#     def __init__(self, course, student) -> None:
#         self.course = course
#         self.student = student
#         self.context = {}
    
#     def get_context(self):
#         try:
#             payment = CoursePayment.objects.get(course=self.course, student=self.student)
#         except CoursePayment.DoesNotExist:
#             self.context['payment'] = consts.COURSE_OPTION_FREE
#         else:
#             self.context['payment'] = payment.option
        
#         return self.context
    

class ExtraContext:
    def __init__(self, context, user, obj) -> None:
        self.context = context
        self.user = user
        self.obj = obj

    def is_author(self):
        return self.user == self.obj.author
    
    def update_context(self):
        self.context['is_author'] = self.is_author()
        self.context['user'] = self.user
        return self.context
    

def get_test_completion_result(context, obj):
    user = context.get('user')
    try:
        test_completion = TestCompletion.objects.get(test=obj, student=user)
    except TestCompletion.DoesNotExist:
        return False
    else:
        return test_completion.result
    

def has_user_full_access(context, instance):
    payment_option = context.get('payment')
    is_author = context.get('is_author')
    return is_author or (payment_option and consts.COURSE_OPTIONS.index(payment_option) >= consts.COURSE_OPTIONS.index(instance.option))