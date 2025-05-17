"""Tailwind CSS form field filter.

Placed temporarily in this app, but should be moved to a more appropriate place.
"""

from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(value, arg):
    """Add a class to a form field."""
    return value.as_widget(attrs={"class": arg})
