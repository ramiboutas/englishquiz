from django.apps import AppConfig


class AffiliatesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "affiliates"

    def ready(self):
        from . import tasks  # noqa