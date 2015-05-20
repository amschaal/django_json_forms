from django.apps import AppConfig

class Config(AppConfig):
    name = 'django_json_forms'
    verbose_name = "Django Json Forms"

    def ready(self):
        import signals