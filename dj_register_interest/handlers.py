"""Register Interest Handlers."""

import logging

from .forms import InterestForm


class RegisterInterestHandler:
    """Wrap logic for registering interest, currently only saves to database.

    Can be expanded to notify project's stakeholders with email, text message, etc.
    """

    _logger = logging.getLogger(__name__)

    def __call__(self, form: InterestForm) -> bool:
        """Entry point."""
        self._logger.info("Saving interest form data %s", form.data)

        if form.is_valid():
            form.save()
            return True

        return False
