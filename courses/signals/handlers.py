from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import SectionItem, Lesson, AdditionalFile


@receiver(post_save, sender=Lesson)
@receiver(post_save, sender=AdditionalFile)
def create_section_item(sender, instance, **kwargs):
    SectionItem.objects.create(content_object=instance, section=instance.section)
