from django.apps import AppConfig


class SharingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sharing'

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals
