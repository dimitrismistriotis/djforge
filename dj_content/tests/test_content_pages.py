"""Test Content Pages."""

import pytest

from django.urls import reverse

pytestmark = [pytest.mark.django_db]


class TestContentPages:
    """Test Content Pages."""

    @pytest.mark.parametrize(
        "url_name",
        [
            "dj_content:health",
            "dj_content:about-us",
        ],
    )
    def test_homepage_returns_200(self, client, url_name) -> None:
        """Test page returns a 200 response."""
        response = client.get(reverse(url_name))

        assert response.status_code == 200
