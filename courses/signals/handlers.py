from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Lesson, AdditionalFile, Test, Homework, Course
from courses.blogic_stripe import delete_stripe_course_item, create_stripe_course_item
from courses.blogic import calculate_video_length, create_section_item


@receiver(post_save, sender=Lesson)
@receiver(post_save, sender=AdditionalFile)
@receiver(post_save, sender=Test)
@receiver(post_save, sender=Homework)
def create_section_item_handler(sender, instance, created, **kwargs):
    if created:
        create_section_item(instance)


@receiver(post_save, sender=Course)
def create_stripe_course_item_handler(sender, instance, created, **kwargs):
    if not created:
        delete_stripe_course_item(instance)
    create_stripe_course_item(instance)


@receiver(post_save, sender=Lesson)
def calculate_video_length_handler(sender, instance, *args, **kwargs):
    calculate_video_length(instance)


