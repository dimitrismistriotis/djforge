"""Custom Exceptions for the dj_emails app."""


class DjEmailException(Exception):
    """Exception occurred while rendering emails."""


class EmailDispatcherException(Exception):
    """Exception occurred while sending emails."""
