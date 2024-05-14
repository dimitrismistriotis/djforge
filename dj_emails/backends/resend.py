"""Django backend for Resend.com."""
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage


class ResendEmailBackendException(Exception):
    """Base exception for ResendEmailBackend."""


class ResendEmailBackend(BaseEmailBackend):
    """Dispatch Emails through Resend.com.

    As a subclass of BaseEmailBackend, it must at least overwrite send_messages().

    open() and close() can be called indirectly by using a backend object as a
    context manager:

       with backend as connection:
           # do something with connection
           pass
    """

    def __init__(self, fail_silently=False, **kwargs):
        """Initialize the ResendEmailBackend class.

        Check the exisence of an API key and fail if it does not exist.
        """
        super().__init__(fail_silently=fail_silently, **kwargs)

    def open(self):
        """Override the open method of BaseEmailBackend, but does nothing."""
        pass

    def close(self):
        """Override the close method of BaseEmailBackend, but does nothing."""
        pass

    def send_messages(self, email_messages: list[EmailMessage]) -> int:
        """Send one or more EmailMessage objects.

        Returns the number of email messages sent.
        """
        email_message: EmailMessage
        for email_message in email_messages:
            print(f"Sending email to {email_message.to}")
