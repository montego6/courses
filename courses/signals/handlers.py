from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import SectionItem, Lesson, AdditionalFile, Test, Homework


# @receiver(post_save, sender=Lesson)
# @receiver(post_save, sender=AdditionalFile)
# @receiver(post_save, sender=Test)
# @receiver(post_save, sender=Homework)
def create_section_item(sender, instance, created, **kwargs):
    if created:
        SectionItem.objects.create(content_object=instance, section=instance.section)
