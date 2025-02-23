"""
App configuration for the videoflix_app.
"""

from django.apps import AppConfig


class VideoflixAppConfig(AppConfig):
    """
    Configuration class for the videoflix_app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "videoflix_app"

    def ready(self):
        """
        Imports signals when the application is ready.
        """
        import videoflix_app.signals  # noqa: F401 (Verhindert unnötige Warnung)
