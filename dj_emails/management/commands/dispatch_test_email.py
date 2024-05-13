"""Dispatch Test Email.

Call from commend line:

python manage.py dispatch_test_email --email dimitrios@mistriotis.com
"""
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):
    """Dispatches test email to the specified email address."""

    help = "Dispatches test email to the specified email address."

    def add_arguments(self, parser):
        """Add arguments to the command."""
        parser.add_argument(
            "--email", type=str, help="Email address to send the test email to."
        )

    def handle(self, *args, **options):
        """Handle the command."""
        email = options["email"]
        print(f"Sending test email to {email}")
        raise CommandError("Test email sending is not implemented.")
