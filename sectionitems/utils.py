from moviepy.editor import VideoFileClip
from sectionitems.models import Lesson, SectionItem, TestCompletion
from core import consts


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