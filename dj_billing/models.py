"""Billing and subscription models for the dj_billing app."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _


class CustomerQuerySet(models.QuerySet):
    """QuerySet for Customer model."""

    def for_user(self, user):
        """Return customers for a specific user."""
        return self.filter(user=user)


class Customer(models.Model):
    """Customer model to store Stripe customer information."""

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer",
        verbose_name=_("User"),
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Stripe Customer ID"),
        help_text=_("The customer ID from Stripe"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    objects = CustomerQuerySet.as_manager()

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        db_table = "dj_billing_customer"

    def __str__(self):
        """Return string representation of the customer."""
        return f"Customer {self.user.email} ({self.stripe_customer_id})"


class PlanQuerySet(models.QuerySet):
    """QuerySet for Plan model."""

    def active(self):
        """Return active plans."""
        return self.filter(is_active=True)


class Plan(models.Model):
    """Plan model to store subscription plan information."""

    id = models.BigAutoField(primary_key=True)
    stripe_product_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Stripe Product ID"),
        help_text=_("The product ID from Stripe (e.g., prod_ABC123)"),
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Display Order"),
        help_text=_(
            "Order in which this plan appears on the pricing page (lower numbers first)"
        ),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this plan is currently available for purchase"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    objects = PlanQuerySet.as_manager()

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")
        db_table = "dj_billing_plan"

    def __str__(self):
        """Return string representation of the plan."""
        stripe_details = self.get_stripe_details()
        return stripe_details.get("name", f"Plan ({self.stripe_product_id})")


    def get_stripe_details(self):
        """Get all product and price details from Stripe."""
        from dj_billing.services import StripeService

        stripe_service = StripeService()
        return stripe_service.get_product_details(self.stripe_product_id)


class SubscriptionQuerySet(models.QuerySet):
    """QuerySet for Subscription model."""

    def active(self):
        """Return active subscriptions."""
        return self.filter(status="active")

    def for_user(self, user):
        """Return subscriptions for a specific user."""
        return self.filter(customer__user=user)


class Subscription(models.Model):
    """Subscription model to store Stripe subscription information."""

    STATUS_CHOICES = [
        ("incomplete", _("Incomplete")),
        ("incomplete_expired", _("Incomplete Expired")),
        ("trialing", _("Trialing")),
        ("active", _("Active")),
        ("past_due", _("Past Due")),
        ("canceled", _("Canceled")),
        ("unpaid", _("Unpaid")),
        ("paused", _("Paused")),
    ]

    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("Customer"),
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("Plan"),
    )
    stripe_subscription_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Stripe Subscription ID"),
        help_text=_("The subscription ID from Stripe"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name=_("Status"),
    )
    current_period_start = models.DateTimeField(
        verbose_name=_("Current Period Start"),
        help_text=_("Start of the current billing period"),
    )
    current_period_end = models.DateTimeField(
        verbose_name=_("Current Period End"),
        help_text=_("End of the current billing period"),
    )
    cancel_at_period_end = models.BooleanField(
        default=False,
        verbose_name=_("Cancel at Period End"),
        help_text=_("Whether the subscription will be canceled at period end"),
    )
    canceled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Canceled At"),
        help_text=_("When the subscription was canceled"),
    )
    trial_start = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Trial Start"),
        help_text=_("Start of the trial period"),
    )
    trial_end = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Trial End"),
        help_text=_("End of the trial period"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    objects = SubscriptionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        db_table = "dj_billing_subscription"

    def __str__(self):
        """Return string representation of the subscription."""
        return f"{self.customer.user.email} - {self.plan} ({self.status})"

    @property
    def is_active(self):
        """Return whether the subscription is active."""
        return self.status in ["active", "trialing"]


class PaymentQuerySet(models.QuerySet):
    """QuerySet for Payment model."""

    def successful(self):
        """Return successful payments."""
        return self.filter(status="succeeded")

    def for_user(self, user):
        """Return payments for a specific user."""
        return self.filter(customer__user=user)


class Payment(models.Model):
    """Payment model to store payment transaction information."""

    STATUS_CHOICES = [
        ("requires_payment_method", _("Requires Payment Method")),
        ("requires_confirmation", _("Requires Confirmation")),
        ("requires_action", _("Requires Action")),
        ("processing", _("Processing")),
        ("requires_capture", _("Requires Capture")),
        ("canceled", _("Canceled")),
        ("succeeded", _("Succeeded")),
    ]

    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Customer"),
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Subscription"),
        null=True,
        blank=True,
    )
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Stripe Payment Intent ID"),
        help_text=_("The payment intent ID from Stripe"),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Amount"),
        help_text=_("Payment amount in USD"),
    )
    currency = models.CharField(
        max_length=3,
        default="usd",
        verbose_name=_("Currency"),
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        verbose_name=_("Status"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Payment description"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    objects = PaymentQuerySet.as_manager()

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        db_table = "dj_billing_payment"
        ordering = ["-created_at"]

    def __str__(self):
        """Return string representation of the payment."""
        return f"Payment ${self.amount} - {self.customer.user.email} ({self.status})"

    @property
    def is_successful(self):
        """Return whether the payment was successful."""
        return self.status == "succeeded"
