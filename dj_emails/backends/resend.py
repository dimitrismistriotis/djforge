"""Django backend for Resend.com."""
import logging

import resend
from resend.exceptions import ResendError

from django.conf import settings
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

    _logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, fail_silently=False, **kwargs):
        """Initialize the ResendEmailBackend class.

        Check the exisence of an API key and fail if it does not exist.
        """
        if not hasattr(settings, "RESEND_API_KEY"):
            raise ResendEmailBackendException(
                "RESEND_API key is not set in settings.py"
            )

        resend.api_key = getattr(settings, "RESEND_API_KEY")

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
        sent_messages = 0

        email_message: EmailMessage
        for email_message in email_messages:
            params: resend.Emails.SendParams = {
                "sender": email_message.from_email,
                "to": email_message.to,
                "subject": email_message.subject,
                "html": email_message.body,
                "reply_to": email_message.reply_to,
                "bcc": email_message.bcc,
                "cc": email_message.cc,
                "tags": [
                    {"name": "environment", "value": getattr(settings, "ENVIRONMENT")},
                    # {"name": "tag2", "value": "tagvalue2"},
                ],
            }
            self._logger.debug("Sending email: %s", params)
            try:
                email = resend.Emails.send(params)
                self._logger.info("Email sent: %s", email)
            except ResendError as resend_error:
                self._logger.exception(resend_error)

                raise ResendEmailBackendException(str(resend_error)) from resend_error

            sent_messages += 1

        return sent_messages
