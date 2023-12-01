from django.db.models.signals import post_save
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
def create_section_item_handler(sender, instance, created, **kwargs):
    if created:
        create_section_item(instance)
        # SectionItem.objects.create(content_object=instance, section=instance.section)

def create_section_item(instance):
    SectionItem.objects.create(content_object=instance, section=instance.section)


def create_stripe_course_item(instance):
    product = stripe.Product.create(name=instance.name)
    price = stripe.Price.create(
        unit_amount=int(instance.price * 100),
        currency='rub',
        product=product['id']
    )
    option_prices = {}
    for idx, option in enumerate(instance.options):
        option_dict = {}
        option_dict['price'] = stripe.Price.create(
        unit_amount=int(option['price'] * 100),
        currency='rub',
        product=product['id']
        )['id']
        if idx > 0:
            upgrade = stripe.Product.create(name=instance.name + ' upgrade to option ' + option['option'])
            option_dict['upgrade'] = {}
            for upgradable_option in instance.options[:idx]:
                upgrade_price = option['price'] - upgradable_option['price']
                price = stripe.Price.create(
                    unit_amount=int(upgrade_price * 100),
                    currency='rub',
                    product=upgrade['id']
                )
                option_dict['upgrade'][upgradable_option['option']] = price['id']
        option_prices[option['option']] = option_dict
    StripeCourse.objects.create(course=instance, product=product['id'], option_prices=option_prices)

def delete_stripe_course_item(instance):
    StripeCourse.objects.filter(course=instance).delete()

@receiver(post_save, sender=Course)
def create_stripe_course_item_handler(sender, instance, created, **kwargs):
    if not created:
        # StripeCourse.objects.filter(course=instance).delete()
        delete_stripe_course_item(instance)
    create_stripe_course_item(instance)
    # product = stripe.Product.create(name=instance.name)
    # price = stripe.Price.create(
    #     unit_amount=int(instance.price * 100),
    #     currency='rub',
    #     product=product['id']
    # )
    # option_prices = {}
    # for idx, option in enumerate(instance.options):
    #     option_dict = {}
    #     option_dict['price'] = stripe.Price.create(
    #     unit_amount=int(option['price'] * 100),
    #     currency='rub',
    #     product=product['id']
    #     )['id']
    #     if idx > 0:
    #         upgrade = stripe.Product.create(name=instance.name + ' upgrade to option ' + option['option'])
    #         option_dict['upgrade'] = {}
    #         for upgradable_option in instance.options[:idx]:
    #             upgrade_price = option['price'] - upgradable_option['price']
    #             price = stripe.Price.create(
    #                 unit_amount=int(upgrade_price * 100),
    #                 currency='rub',
    #                 product=upgrade['id']
    #             )
    #             option_dict['upgrade'][upgradable_option['option']] = price['id']
    #     option_prices[option['option']] = option_dict
    # StripeCourse.objects.create(course=instance, product=product['id'], option_prices=option_prices)


@receiver(post_save, sender=Lesson)
def calculate_video_length_handler(sender, instance, *args, **kwargs):
    calculate_video_length(instance)


def calculate_video_length(instance):
    video = VideoFileClip(instance.file.path)
    Lesson.objects.filter(id=instance.id).update(duration=video.duration)