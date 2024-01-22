from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from courses.helpers import generate_course_slug
from courses.models import Course
from courses.blogic_stripe import delete_stripe_course_item, create_stripe_course_item


@receiver(post_save, sender=Course)
def create_stripe_course_item_handler(sender, instance, created, **kwargs):
    if not created:
        delete_stripe_course_item(instance)
    create_stripe_course_item(instance)


@receiver(pre_save, sender=Course)
def generate_course_slug_handler(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_course_slug(instance)




