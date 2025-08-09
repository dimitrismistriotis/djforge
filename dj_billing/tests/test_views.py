"""Tests for dj_billing views."""

import pytest

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from ..services import StripeService

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestBillingView:
    """Test billing views."""

    def test_billing_view_requires_login(self) -> None:
        """Test that billing view requires authentication."""
        client = Client()
        url = reverse("dj_billing:pricing")
        response = client.get(url)
        assert response.status_code == 302  # Redirect to login

    def test_billing_view_authenticated(self, mocker) -> None:
        """Test billing view for authenticated user."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        client = Client()
        client.force_login(user)
        url = reverse("dj_billing:pricing")

        mock_get_customer = mocker.patch.object(StripeService, "get_or_create_customer")
        mock_customer = mocker.Mock()
        mock_customer.payments.all.return_value = []
        mock_get_customer.return_value = mock_customer

        response = client.get(url)

        assert response.status_code == 200
        assert "Products & Subscription" in response.content.decode()
