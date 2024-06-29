"""Functions related to permission checks for the dj_users app."""

from functools import wraps
from typing import Callable

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def is_platform_admin(user) -> bool:
    """Check if user is a platform administrator."""
    return user.groups.filter(name="Platform Administrators").exists()


#
# Define decorators for permission checks:
#
restrict_to_platform_admin = user_passes_test(is_platform_admin)


def restrict_to_platform_admin_404(view_func) -> Callable:
    """Restrict view to Platform Administrators, raise 404 if not."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if is_platform_admin(request.user):
            return view_func(request, *args, **kwargs)

        #
        # Should log at this point
        #
        raise PermissionDenied()

    return wrapper
