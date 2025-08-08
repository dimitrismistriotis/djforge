"""Tests for dj_billing services."""

import pytest

from django.contrib.auth import get_user_model

from ..models import Customer
from ..services import StripeService

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestStripeService:
    """Test StripeService functionality."""

    def test_create_customer(self, mocker) -> None:
        """Test creating a Stripe customer."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="testpass123",
        )
        stripe_service = StripeService()

        mock_stripe_customer = mocker.Mock()
        mock_stripe_customer.id = "cus_test_123"

        mock_stripe_create = mocker.patch("dj_billing.services.stripe.Customer.create")
        mock_stripe_create.return_value = mock_stripe_customer

        customer = stripe_service.create_customer(user)

        assert customer.user == user
        assert customer.stripe_customer_id == "cus_test_123"

        mock_stripe_create.assert_called_once_with(
            email=user.email,
            name="Test User",
            metadata={"user_id": user.id},
        )

    def test_get_or_create_customer_existing(self, mocker) -> None:
        """Test getting existing customer."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        existing_customer = Customer.objects.create(
            user=user,
            stripe_customer_id="cus_existing_123",
        )
        stripe_service = StripeService()

        mock_stripe_create = mocker.patch("dj_billing.services.stripe.Customer.create")
        customer = stripe_service.get_or_create_customer(user)

        assert customer == existing_customer
        mock_stripe_create.assert_not_called()

    def test_get_or_create_customer_new(self, mocker) -> None:
        """Test creating new customer when none exists."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        stripe_service = StripeService()

        mock_stripe_customer = mocker.Mock()
        mock_stripe_customer.id = "cus_test_123"

        mock_stripe_create = mocker.patch("dj_billing.services.stripe.Customer.create")
        mock_stripe_create.return_value = mock_stripe_customer

        customer = stripe_service.get_or_create_customer(user)

        assert customer.user == user
        assert customer.stripe_customer_id == "cus_test_123"
        mock_stripe_create.assert_called_once()
