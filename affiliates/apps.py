from django.apps import AppConfig


class AffiliatesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "affiliates"
    verbose_name = "00 Affiliates"

    def ready(self):
        from . import tasks  # noqa
