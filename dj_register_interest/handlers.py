"""Register Interest Handlers."""
from .forms import InterestForm


class RegisterInterestHandler:
    """Wrap logic for registering interest, currently only saves to database.

    Can be expanded to notify project's stakeholders with email, text message, etc.
    """

    def __call__(self, form: InterestForm) -> bool:
        """Entry point"""
        if form.is_valid():
            form.save()
            return True

        return False
