from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from courses.models import SectionItem, Lesson, AdditionalFile, Test, Homework, Course, StripeCourse
import stripe
from decouple import config
from moviepy.editor import VideoFileClip

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
    option_prices = {}
    for option in instance.options:
        price = stripe.Price.create(
        unit_amount=int(option['price'] * 100),
        currency='rub',
        product=product['id']
        )
        option_prices[option['option']] = price['id']
    StripeCourse.objects.create(course=instance, product=product['id'], price=price['id'], option_prices=option_prices)


@receiver(post_save, sender=Lesson)
def calculate_video_length(sender, instance, *args, **kwargs):
    video = VideoFileClip(instance.file.path)
    Lesson.objects.filter(id=instance.id).update(duration=video.duration)

