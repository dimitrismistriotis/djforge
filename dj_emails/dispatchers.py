"""Email Dispatchers, other modules should have a corresponding dispatcher here."""
import logging
from smtplib import SMTPException

from django.core.mail import send_mail
from django.core.mail import mail_admins
from django.conf import settings

from .exceptions import EmailDispatcherException


def contact_us_email_dispatcher(email: str, name: str, message: str) -> None:
    """Dispatches the email to the contact us initiator and to platform admins.

    >>> from dj_emails.dispatchers import contact_us_email_dispatcher
    >>> contact_us_email_dispatcher("person@example.com", "Does the platform support X")
    """
    if not getattr(settings, "DISPATCHING_EMAILS", False):
        logging.getLogger(__name__).info(
            (
                "Contact Us emails are not being dispatched, "
                "as DISPATCHING_EMAILS is False."
                "Target email: %s, Name: %s, Message: %s"
            ),
            email,
            name,
            message,
        )
        return

    email_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    try:
        send_mail(
            subject="New Contact Form Submission",
            message=email_message,
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
            html_message=f"<p>This is a Contact Us email from DJ-Forge - html. {email_message}</p>",
        )
        mail_admins(
            subject="New Contact Form Submission",
            message=email_message,
            fail_silently=False,
            html_message=f"<p>This is a Contact Us email from DJ-Forge - html. {email_message}</p>",
        )
    except SMTPException as smtp_exception:
        raise EmailDispatcherException(str(smtp_exception)) from smtp_exception
    except Exception as exception:
        raise EmailDispatcherException(str(exception)) from exception
