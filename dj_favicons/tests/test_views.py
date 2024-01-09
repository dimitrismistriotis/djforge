"""Test for the views of the dj_favicons app."""
from django.test import Client


class TestFaviconViews:
    """Test for the favicon view."""

    def test_favicon(self, client: Client) -> None:
        """Test the favicon view."""
        response = client.get("/favicon.ico")

        assert response.status_code == 200
