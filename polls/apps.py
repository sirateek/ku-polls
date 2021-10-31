"""The Django application config for Polls app."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Polls app Django config object."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        import polls.signals.handlers
