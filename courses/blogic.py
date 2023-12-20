import stripe
from moviepy.editor import VideoFileClip
from decouple import config
from courses import consts
from courses.models import CoursePayment, Lesson, SectionItem,  TestCompletion


stripe.api_key = config('STRIPE_KEY')
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
        payment = CoursePayment.objects.get(course=course, student=student)
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
    

def get_test_completion_result(context, test):
    user = context.get('user')
    try:
        test_completion = TestCompletion.objects.get(test=test, student=user)
    except TestCompletion.DoesNotExist:
        return False
    else:
        return test_completion.result
    

def has_user_full_access(context, instance):
    payment_option = context.get('payment', consts.COURSE_OPTION_FREE)
    is_author = context.get('is_author', False)
    return is_author or (payment_option and consts.COURSE_OPTIONS.index(payment_option) >= consts.COURSE_OPTIONS.index(instance.option))


def calculate_video_length(instance):
    video = VideoFileClip(instance.file.path)
    Lesson.objects.filter(id=instance.id).update(duration=video.duration)
    video.close()


def create_section_item(instance):
    SectionItem.objects.create(content_object=instance, section=instance.section)