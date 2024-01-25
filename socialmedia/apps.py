from __future__ import annotations

from django.apps import AppConfig


class socialmediaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "socialmedia"
    verbose_name = "00 Social media"

    def ready(self):
        from . import tasks  # noqa
