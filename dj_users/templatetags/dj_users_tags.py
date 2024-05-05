"""Template tags for the dj_users app.

To include these tags in a template, add `{% load dj_users_tags %}` at the top.
"""
from django import template
from django.conf import settings

register = template.Library()


def display_action_requiring_email_dispatch() -> bool:
    """Display action requiring email dispatch based settings value.

    Currently retrieves from ACCOUNT_EMAIL_VERIFICATION of AllAuth.

    Use:

    {% load dj_users_tags %}

    ...

    {% if display_action_requiring_email_dispatch %}
        <!-- Display action requiring email dispatch -->
    {% endif %}
    """
    return getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", "none") != "none"
