"""AppConfig for dj_users app."""
from django.apps import AppConfig


class DjUsersConfig(AppConfig):
    """AppConfig for dj_users app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "dj_users"

    def ready(self) -> None:
        """When app is ready execute the following."""
        super().ready()

        from .seed import create_platform_administrators_group

        create_platform_administrators_group()
