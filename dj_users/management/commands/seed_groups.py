"""Seed Groups.

Call from commend line:

python manage.py seed_groups
"""

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from ...seed import create_platform_administrators_group


class Command(BaseCommand):
    """Create Group "Platform Administrators" if not there.

    Currently there is only one group required,
    should be extended here if more groups are required.
    """

    help = 'Create Group "Platform Administrators" if not there.'

    def handle(self, *args, **options):
        """Handle the command."""
        print("Seeding Groups...")
        print()

        try:
            create_platform_administrators_group()
        except Exception as exception:
            raise CommandError(f"Error creaating groups: {exception}")
