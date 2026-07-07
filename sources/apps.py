from django.apps import AppConfig


class SourcesConfig(AppConfig):
    name = 'sources'
    verbose_name = 'Управление источниками'

    def ready(self):
        import sources.signals