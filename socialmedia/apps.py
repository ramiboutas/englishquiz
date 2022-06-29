from django.apps import AppConfig


class socialmediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'socialmedia'

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals
