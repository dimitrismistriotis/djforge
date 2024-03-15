"""Conftest for dj_dashboard tests."""

import pytest

from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


@pytest.fixture
def regular_user() -> USER_MODEL:
    """Fixture for non admin User."""
    return USER_MODEL.objects.create_user(
        username="person@example.com",
        email="person@example.com",
        password="correct_password_for_person",
    )
