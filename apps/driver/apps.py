from django.apps import AppConfig


class DriverConfig(AppConfig):
    name = 'apps.driver'

    def ready(self):
        from apps.domain.handlers import register_domain_handlers

        register_domain_handlers()
