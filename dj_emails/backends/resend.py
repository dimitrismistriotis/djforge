"""Django backend for Resend.com."""

import logging

import resend
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.base import BaseEmailBackend
from resend.exceptions import ResendError


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
    _default_from_email: str = getattr(settings, "DEFAULT_FROM_EMAIL")

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

    def send_messages(self, email_messages: list[EmailMultiAlternatives]) -> int:
        """Send one or more EmailMultiAlternatives objects.

        Returns the number of email messages sent.
        """
        messages_count = 0

        email_message: EmailMultiAlternatives
        for email_message in email_messages:
            html_content = next(
                map(
                    lambda x: x[0],
                    filter(lambda x: x[1] == "text/html", email_message.alternatives),
                ),
                None,
            )
            # print(f"{html_content=}")

            params: resend.Emails.SendParams = {
                "sender": email_message.from_email or self._default_from_email,
                "to": email_message.to,
                "subject": email_message.subject,
                "text": email_message.body,
                "reply_to": email_message.reply_to,
                "bcc": email_message.bcc,
                "cc": email_message.cc,
                "tags": [
                    {"name": "environment", "value": getattr(settings, "ENVIRONMENT")},
                    # {"name": "tag2", "value": "tagvalue2"},
                ],
            }

            if html_content:
                params["html"] = html_content

            self._logger.debug("Sending email: %s", params)
            try:
                email = resend.Emails.send(params)
                self._logger.info("Email sent: %s", email)
            except ResendError as resend_error:
                self._logger.exception(resend_error)

                raise ResendEmailBackendException(str(resend_error)) from resend_error

            messages_count += 1

        return messages_count
