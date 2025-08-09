"""Tests for dj_billing models."""

from decimal import Decimal

import pytest

from django.contrib.auth import get_user_model

from ..models import Customer
from ..models import Payment
from ..models import Plan
from ..models import Subscription

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestPlan:
    """Test Plan model functionality."""

    def test_plan_creation(self) -> None:
        """Test creating a plan."""
        plan = Plan.objects.create(
            stripe_product_id="prod_test_123",
            order=1,
        )

        assert plan.stripe_product_id == "prod_test_123"
        assert plan.order == 1
        assert plan.is_active is True

    def test_plan_str_representation(self, mocker) -> None:
        """Test plan string representation."""
        mock_product = mocker.Mock()
        mock_product.name = "Test Product"
        mock_product.description = "Test description"

        mock_product_retrieve = mocker.patch(
            "dj_billing.services.stripe.Product.retrieve"
        )
        mock_price_list = mocker.patch("dj_billing.services.stripe.Price.list")

        mock_product_retrieve.return_value = mock_product
        mock_price_list.return_value.data = []

        plan = Plan.objects.create(
            stripe_product_id="prod_test_123",
            order=1,
        )
        assert str(plan) == "Test Product"

    def test_active_plans_queryset(self) -> None:
        """Test active plans queryset method."""
        Plan.objects.create(
            stripe_product_id="prod_test_123",
            order=1,
        )
        Plan.objects.create(
            stripe_product_id="prod_test_456",
            order=2,
            is_active=False,
        )

        active_plans = Plan.objects.active()
        assert active_plans.count() == 1
        assert active_plans.first().is_active is True


class TestCustomer:
    """Test Customer model functionality."""

    def test_customer_creation(self) -> None:
        """Test creating a customer."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        customer = Customer.objects.create(
            user=user,
            stripe_customer_id="cus_test_123",
        )

        assert customer.user == user
        assert customer.stripe_customer_id == "cus_test_123"

    def test_customer_str_representation(self) -> None:
        """Test customer string representation."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        customer = Customer.objects.create(
            user=user,
            stripe_customer_id="cus_test_123",
        )
        expected = f"Customer {user.email} (cus_test_123)"
        assert str(customer) == expected

    def test_for_user_queryset(self) -> None:
        """Test for_user queryset method."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        customer = Customer.objects.create(
            user=user,
            stripe_customer_id="cus_test_123",
        )

        customers = Customer.objects.for_user(user)
        assert customers.count() == 1
        assert customers.first() == customer


class TestSubscription:
    """Test Subscription model functionality."""

    def test_subscription_creation(self) -> None:
        """Test creating a subscription."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        customer = Customer.objects.create(
            user=user,
            stripe_customer_id="cus_test_123",
        )
        plan = Plan.objects.create(
            stripe_product_id="prod_test_123",
            order=1,
        )
        subscription = Subscription.objects.create(
            customer=customer,
            plan=plan,
            stripe_subscription_id="sub_test_123",
            status=Subscription.Status.ACTIVE,
            current_period_start="2023-01-01T00:00:00Z",
            current_period_end="2023-02-01T00:00:00Z",
        )

        assert subscription.customer == customer
        assert subscription.plan == plan
        assert subscription.status == "active"
        assert subscription.is_active is True

    def test_subscription_is_active_property(self) -> None:
        """Test subscription is_active property."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        customer = Customer.objects.create(
            user=user,
            stripe_customer_id="cus_test_123",
        )
        plan = Plan.objects.create(
            stripe_product_id="prod_test_123",
            order=1,
        )

        active_subscription = Subscription.objects.create(
            customer=customer,
            plan=plan,
            stripe_subscription_id="sub_test_123",
            status=Subscription.Status.ACTIVE,
            current_period_start="2023-01-01T00:00:00Z",
            current_period_end="2023-02-01T00:00:00Z",
        )

        trial_subscription = Subscription.objects.create(
            customer=customer,
            plan=plan,
            stripe_subscription_id="sub_test_456",
            status=Subscription.Status.TRIALING,
            current_period_start="2023-01-01T00:00:00Z",
            current_period_end="2023-02-01T00:00:00Z",
        )

        canceled_subscription = Subscription.objects.create(
            customer=customer,
            plan=plan,
            stripe_subscription_id="sub_test_789",
            status=Subscription.Status.CANCELED,
            current_period_start="2023-01-01T00:00:00Z",
            current_period_end="2023-02-01T00:00:00Z",
        )

        assert active_subscription.is_active is True
        assert trial_subscription.is_active is True
        assert canceled_subscription.is_active is False


class TestPayment:
    """Test Payment model functionality."""

    def test_payment_creation(self) -> None:
        """Test creating a payment."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        customer = Customer.objects.create(
            user=user,
            stripe_customer_id="cus_test_123",
        )
        payment = Payment.objects.create(
            customer=customer,
            stripe_payment_intent_id="pi_test_123",
            amount=Decimal("29.99"),
            currency="usd",
            status=Payment.Status.SUCCEEDED,
            description="Test payment",
        )

        assert payment.customer == customer
        assert payment.amount == Decimal("29.99")
        assert payment.status == Payment.Status.SUCCEEDED
        assert payment.is_successful is True

    def test_payment_is_successful_property(self) -> None:
        """Test payment is_successful property."""
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        customer = Customer.objects.create(
            user=user,
            stripe_customer_id="cus_test_123",
        )

        successful_payment = Payment.objects.create(
            customer=customer,
            stripe_payment_intent_id="pi_test_123",
            amount=Decimal("29.99"),
            currency="usd",
            status=Payment.Status.SUCCEEDED,
        )

        failed_payment = Payment.objects.create(
            customer=customer,
            stripe_payment_intent_id="pi_test_456",
            amount=Decimal("29.99"),
            currency="usd",
            status=Payment.Status.CANCELED,
        )

        assert successful_payment.is_successful
        assert not failed_payment.is_successful
