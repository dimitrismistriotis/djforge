"""Utility functions for Dj Users."""

from pathlib import Path
from typing import Union
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
import json


def is_member(user, group_name):
    """Check if user is a member of a group."""
    return user.groups.filter(name=group_name).exists()


def create_permission(
    codename: str, name: str, content_type: ContentType
) -> Permission:
    """Return permission object."""
    return Permission.objects.create(
        codename=codename,
        name=codename,
        content_type=content_type,
    )


def load_json(path_to_file: Union[str, Path]) -> dict[str, str]:
    """Load a json file and return a dict."""
    with open(path_to_file, encoding="utf-8") as f:
        j = json.load(f)
    return j
