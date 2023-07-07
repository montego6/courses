from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import SectionItem, Lesson, AdditionalFile, Test, Homework, Course, StripeCourse
import stripe
from decouple import config

stripe.api_key = config('STRIPE_KEY')


@receiver(post_save, sender=Lesson)
@receiver(post_save, sender=AdditionalFile)
@receiver(post_save, sender=Test)
@receiver(post_save, sender=Homework)
def create_section_item(sender, instance, created, **kwargs):
    if created:
        SectionItem.objects.create(content_object=instance, section=instance.section)


@receiver(post_save, sender=Course)
def create_stripe_course_item(sender, instance, created, **kwargs):
    if not created:
        StripeCourse.objects.filter(course=instance).delete()
    product = stripe.Product.create(name=instance.name)
    price = stripe.Price.create(
        unit_amount=int(instance.price * 100),
        currency='rub',
        product=product['id']
    )
    StripeCourse.objects.create(course=instance, product=product['id'], price=price['id'])
