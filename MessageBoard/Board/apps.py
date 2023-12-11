from django.apps import AppConfig


class BoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Board'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов
