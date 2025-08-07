"""Tests for dj_billing views."""

from unittest.mock import Mock
from unittest.mock import patch

import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..services import StripeService

User = get_user_model()

pytestmark = pytest.mark.django_db


class BillingViewTest(TestCase):
    """Test billing views."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )

    def test_billing_view_requires_login(self) -> None:
        """Test that billing view requires authentication."""
        url = reverse("dj_billing:pricing")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_billing_view_authenticated(self) -> None:
        """Test billing view for authenticated user."""
        self.client.force_login(self.user)
        url = reverse("dj_billing:pricing")

        with patch.object(StripeService, "get_or_create_customer") as mock_get_customer:
            mock_customer = Mock()
            mock_customer.payments.all.return_value = []
            mock_get_customer.return_value = mock_customer

            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Products & Subscription")
