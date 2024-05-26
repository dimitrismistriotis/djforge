"""Functions related to permission checks for the dj_users app."""
from django.contrib.auth.decorators import user_passes_test


def is_platform_admin(user) -> bool:
    """Check if user is a platform administrator."""
    return user.groups.filter(name="Platform Administrators").exists()


#
# Define decorator(s) for permission checks:
#
restrict_to_platform_admin = user_passes_test(is_platform_admin)
