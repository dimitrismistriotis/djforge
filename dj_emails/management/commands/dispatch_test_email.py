"""Dispatch Test Email.

Call from commend line:

python manage.py dispatch_test_email --email dimitrios@mistriotis.com
"""
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from rich import print as rich_print


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
        rich_print(f"Sending test email to [bold]{email}[/bold]")

        try:
            send_mail(
                subject="DJ-Forge Test Email",
                message="This is a test email from DJ-Forge - message.",
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
                html_message="<p>This is a test email from DJ-Forge - html.</p>",
            )
        except Exception as exception:
            raise CommandError(f"Error sending email: {exception}")
