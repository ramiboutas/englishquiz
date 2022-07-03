from django.apps import AppConfig


class PuputAppConfig(AppConfig):
    name = 'puput'
    verbose_name = 'puput'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        import puput.signals  # noqa: F401
