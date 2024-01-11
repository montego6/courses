from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Course
from courses.blogic_stripe import delete_stripe_course_item, create_stripe_course_item


@receiver(post_save, sender=Course)
def create_stripe_course_item_handler(sender, instance, created, **kwargs):
    if not created:
        delete_stripe_course_item(instance)
    create_stripe_course_item(instance)





