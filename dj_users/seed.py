"""Seed function for dj_users app, Seeding Groups, Permissions, etc."""

from rich import print as rich_print

from django.contrib.auth.models import Group
from django.db import transaction


@transaction.atomic
def create_platform_administrators_group() -> None:
    """Create a group named "Platform Administrators if not there."""
    group, created = Group.objects.get_or_create(name="Platform Administrators")
    if created:
        rich_print("Group '[red]Platform Administrators[/red]' [bold]created[/bold].")
    else:
        rich_print("Group '[red]Platform Administrators[/red]' already exists.")
