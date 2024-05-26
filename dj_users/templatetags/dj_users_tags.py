"""Template tags for the dj_users app.

To include these tags in a template, add `{% load dj_users_tags %}` at the top.
"""
from django import template
from django.conf import settings
from django.contrib.auth.models import Group

register = template.Library()


@register.simple_tag
def display_action_requiring_email_dispatch() -> bool:
    """Display action requiring email dispatch based settings value.

    Currently retrieves from ACCOUNT_EMAIL_VERIFICATION of AllAuth.

    Use:

    {% load dj_users_tags %}

    ...

    {% display_action_requiring_email_dispatch as can_do_something %}

    {% if can_do_something %}
      <!-- Display action requiring email dispatch -->
    {% endif %}
    """
    return getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", "none") != "none"


@register.filter(name="has_group")
def has_group(user, group_name) -> bool:
    """Check if User Belongs to Given Group.

    This should be avoided as it is better to have specific permissions attached
    to models.

    Use:

    {% load dj_users_tags %}

    ...

    {% if request.user|has_group:"mygroup" %}
      <p>User belongs to my group
    {% else %}
      <p>User doesn't belong to mygroup</p>
    {% endif %}
    """
    if group := Group.objects.filter(name=group_name).first():
        return group in user.groups.all()

    return False
