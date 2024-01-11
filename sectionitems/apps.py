from django.apps import AppConfig


class SectionitemsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sectionitems"

    def ready(self):
        import sectionitems.signals.handlers