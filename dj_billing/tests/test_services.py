"""Tests for dj_billing services."""

from unittest.mock import Mock
from unittest.mock import patch

import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Customer
from ..services import StripeService

User = get_user_model()

pytestmark = pytest.mark.django_db


class StripeServiceTest(TestCase):
    """Test StripeService functionality."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="testpass123",
        )
        self.service = StripeService()

    def test_create_customer(self) -> None:
        """Test creating a Stripe customer."""
        mock_stripe_customer = Mock()
        mock_stripe_customer.id = "cus_test_123"

        with patch("dj_billing.services.stripe.Customer.create") as mock_stripe_create:
            mock_stripe_create.return_value = mock_stripe_customer

            customer = self.service.create_customer(self.user)

            self.assertEqual(customer.user, self.user)
            self.assertEqual(customer.stripe_customer_id, "cus_test_123")

            mock_stripe_create.assert_called_once_with(
                email=self.user.email,
                name="Test User",
                metadata={"user_id": self.user.id},
            )

    def test_get_or_create_customer_existing(self) -> None:
        """Test getting existing customer."""
        existing_customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id="cus_existing_123",
        )

        with patch("dj_billing.services.stripe.Customer.create") as mock_stripe_create:
            customer = self.service.get_or_create_customer(self.user)

            self.assertEqual(customer, existing_customer)
            mock_stripe_create.assert_not_called()

    def test_get_or_create_customer_new(self) -> None:
        """Test creating new customer when none exists."""
        mock_stripe_customer = Mock()
        mock_stripe_customer.id = "cus_test_123"

        with patch("dj_billing.services.stripe.Customer.create") as mock_stripe_create:
            mock_stripe_create.return_value = mock_stripe_customer

            customer = self.service.get_or_create_customer(self.user)

            self.assertEqual(customer.user, self.user)
            self.assertEqual(customer.stripe_customer_id, "cus_test_123")
            mock_stripe_create.assert_called_once()
