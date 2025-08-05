"""Tests for dj_billing app."""

from decimal import Decimal
from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Customer
from .models import Payment
from .models import Plan
from .models import Subscription
from .services import StripeService

User = get_user_model()


class PlanModelTest(TestCase):
    """Test Plan model functionality."""

    def setUp(self) -> None:
        """Set up test data."""
        self.plan_data = {
            "stripe_product_id": "prod_test_123",
            "order": 1,
        }

    def test_plan_creation(self) -> None:
        """Test creating a plan."""
        plan = Plan.objects.create(**self.plan_data)

        self.assertEqual(plan.stripe_product_id, "prod_test_123")
        self.assertEqual(plan.order, 1)
        self.assertTrue(plan.is_active)

    @patch("dj_billing.services.stripe.Product.retrieve")
    @patch("dj_billing.services.stripe.Price.list")
    def test_plan_str_representation(self, mock_price_list, mock_product_retrieve) -> None:
        """Test plan string representation."""
        # Mock Stripe API responses
        mock_product = Mock()
        mock_product.name = "Test Product"
        mock_product.description = "Test description"
        mock_product_retrieve.return_value = mock_product
        
        mock_price_list.return_value.data = []
        
        plan = Plan.objects.create(**self.plan_data)
        self.assertEqual(str(plan), "Test Product")

    def test_active_plans_queryset(self) -> None:
        """Test active plans queryset method."""
        Plan.objects.create(**self.plan_data)
        inactive_plan_data = self.plan_data.copy()
        inactive_plan_data["stripe_product_id"] = "prod_test_456"
        inactive_plan_data["is_active"] = False
        Plan.objects.create(**inactive_plan_data)

        active_plans = Plan.objects.active()
        self.assertEqual(active_plans.count(), 1)
        self.assertTrue(active_plans.first().is_active)


class CustomerModelTest(TestCase):
    """Test Customer model functionality."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

    def test_customer_creation(self) -> None:
        """Test creating a customer."""
        customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id="cus_test_123",
        )

        self.assertEqual(customer.user, self.user)
        self.assertEqual(customer.stripe_customer_id, "cus_test_123")

    def test_customer_str_representation(self) -> None:
        """Test customer string representation."""
        customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id="cus_test_123",
        )
        expected = f"Customer {self.user.email} (cus_test_123)"
        self.assertEqual(str(customer), expected)

    def test_for_user_queryset(self) -> None:
        """Test for_user queryset method."""
        customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id="cus_test_123",
        )

        customers = Customer.objects.for_user(self.user)
        self.assertEqual(customers.count(), 1)
        self.assertEqual(customers.first(), customer)


class SubscriptionModelTest(TestCase):
    """Test Subscription model functionality."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        self.customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id="cus_test_123",
        )
        self.plan = Plan.objects.create(
            stripe_product_id="prod_test_123",
            order=1,
        )

    def test_subscription_creation(self) -> None:
        """Test creating a subscription."""
        subscription = Subscription.objects.create(
            customer=self.customer,
            plan=self.plan,
            stripe_subscription_id="sub_test_123",
            status="active",
            current_period_start="2023-01-01T00:00:00Z",
            current_period_end="2023-02-01T00:00:00Z",
        )

        self.assertEqual(subscription.customer, self.customer)
        self.assertEqual(subscription.plan, self.plan)
        self.assertEqual(subscription.status, "active")
        self.assertTrue(subscription.is_active)

    def test_subscription_is_active_property(self) -> None:
        """Test subscription is_active property."""
        active_subscription = Subscription.objects.create(
            customer=self.customer,
            plan=self.plan,
            stripe_subscription_id="sub_test_123",
            status="active",
            current_period_start="2023-01-01T00:00:00Z",
            current_period_end="2023-02-01T00:00:00Z",
        )

        trial_subscription = Subscription.objects.create(
            customer=self.customer,
            plan=self.plan,
            stripe_subscription_id="sub_test_456",
            status="trialing",
            current_period_start="2023-01-01T00:00:00Z",
            current_period_end="2023-02-01T00:00:00Z",
        )

        canceled_subscription = Subscription.objects.create(
            customer=self.customer,
            plan=self.plan,
            stripe_subscription_id="sub_test_789",
            status="canceled",
            current_period_start="2023-01-01T00:00:00Z",
            current_period_end="2023-02-01T00:00:00Z",
        )

        self.assertTrue(active_subscription.is_active)
        self.assertTrue(trial_subscription.is_active)
        self.assertFalse(canceled_subscription.is_active)


class BillingViewTest(TestCase):
    """Test billing views."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(
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


class StripeServiceTest(TestCase):
    """Test StripeService functionality."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="testpass123",
        )
        self.service = StripeService()

    @patch("dj_billing.services.stripe.Customer.create")
    def test_create_customer(self, mock_stripe_create) -> None:
        """Test creating a Stripe customer."""
        mock_stripe_customer = Mock()
        mock_stripe_customer.id = "cus_test_123"
        mock_stripe_create.return_value = mock_stripe_customer

        customer = self.service.create_customer(self.user)

        self.assertEqual(customer.user, self.user)
        self.assertEqual(customer.stripe_customer_id, "cus_test_123")

        mock_stripe_create.assert_called_once_with(
            email=self.user.email,
            name="Test User",
            metadata={"user_id": self.user.id},
        )

    @patch("dj_billing.services.stripe.Customer.create")
    def test_get_or_create_customer_existing(self, mock_stripe_create) -> None:
        """Test getting existing customer."""
        existing_customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id="cus_existing_123",
        )

        customer = self.service.get_or_create_customer(self.user)

        self.assertEqual(customer, existing_customer)
        mock_stripe_create.assert_not_called()

    @patch("dj_billing.services.stripe.Customer.create")
    def test_get_or_create_customer_new(self, mock_stripe_create) -> None:
        """Test creating new customer when none exists."""
        mock_stripe_customer = Mock()
        mock_stripe_customer.id = "cus_test_123"
        mock_stripe_create.return_value = mock_stripe_customer

        customer = self.service.get_or_create_customer(self.user)

        self.assertEqual(customer.user, self.user)
        self.assertEqual(customer.stripe_customer_id, "cus_test_123")
        mock_stripe_create.assert_called_once()


class PaymentModelTest(TestCase):
    """Test Payment model functionality."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        self.customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id="cus_test_123",
        )

    def test_payment_creation(self) -> None:
        """Test creating a payment."""
        payment = Payment.objects.create(
            customer=self.customer,
            stripe_payment_intent_id="pi_test_123",
            amount=Decimal("29.99"),
            currency="usd",
            status="succeeded",
            description="Test payment",
        )

        self.assertEqual(payment.customer, self.customer)
        self.assertEqual(payment.amount, Decimal("29.99"))
        self.assertEqual(payment.status, "succeeded")
        self.assertTrue(payment.is_successful)

    def test_payment_is_successful_property(self) -> None:
        """Test payment is_successful property."""
        successful_payment = Payment.objects.create(
            customer=self.customer,
            stripe_payment_intent_id="pi_test_123",
            amount=Decimal("29.99"),
            currency="usd",
            status="succeeded",
        )

        failed_payment = Payment.objects.create(
            customer=self.customer,
            stripe_payment_intent_id="pi_test_456",
            amount=Decimal("29.99"),
            currency="usd",
            status="canceled",
        )

        self.assertTrue(successful_payment.is_successful)
        self.assertFalse(failed_payment.is_successful)
