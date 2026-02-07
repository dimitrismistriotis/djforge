"""Stripe service module for handling Stripe API operations."""

import logging
from decimal import Decimal
from zoneinfo import ZoneInfo

import stripe

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Customer
from .models import Payment
from .models import Plan
from .models import Subscription

logger = logging.getLogger(__name__)

User = get_user_model()

# Constants
STRIPE_CENTS_TO_DOLLARS = Decimal("0.01")


class StripeService:
    """Service class for handling Stripe operations."""

    def __init__(self):
        """Initialize Stripe service with API key."""
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_customer(self, user: User) -> Customer:
        """Create a Stripe customer and local Customer record."""
        try:
            # Create customer in Stripe
            stripe_customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.first_name} {user.last_name}".strip(),
                metadata={"user_id": user.id},
            )

            # Create local Customer record
            customer = Customer.objects.create(
                user=user,
                stripe_customer_id=stripe_customer.id,
            )

            logger.info(
                "Created Stripe customer %s for user %s",
                stripe_customer.id,
                user.email,
            )
            return customer

        except stripe.error.StripeError as exception:
            logger.error(
                "Failed to create Stripe customer for user %s: %s",
                user.email,
                exception,
            )
            raise

    def get_or_create_customer(self, user: User) -> Customer:
        """Get existing customer or create a new one."""
        try:
            return Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            return self.create_customer(user)

    def create_checkout_session(
        self,
        customer: Customer,
        plan: Plan,
        success_url: str,
        cancel_url: str,
        trial_period_days: int = 0,
    ) -> str:
        """Create a Stripe checkout session for subscription."""
        try:
            # Get the price ID from the plan's Stripe product details
            stripe_details = plan.get_stripe_details()
            price_details = stripe_details.get("price_details", {})
            price_id = price_details.get("price_id")

            if not price_id:
                raise ValueError(f"No price found for plan {plan.stripe_product_id}")

            session_data = {
                "customer": customer.stripe_customer_id,
                "payment_method_types": ["card"],
                "line_items": [
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                "mode": "subscription",
                "success_url": success_url,
                "cancel_url": cancel_url,
                "metadata": {
                    "user_id": customer.user.id,
                    "plan_id": plan.id,
                },
            }

            if trial_period_days > 0:
                session_data["subscription_data"] = {
                    "trial_period_days": trial_period_days,
                }

            session = stripe.checkout.Session.create(**session_data)

            logger.info(
                f"Created checkout session {session.id} for customer {customer.stripe_customer_id}"
            )
            return session.url

        except stripe.error.StripeError as exception:
            logger.error(
                f"Failed to create checkout session for customer {customer.stripe_customer_id}: {exception}"
            )
            raise

    def create_billing_portal_session(
        self,
        customer: Customer,
        return_url: str,
    ) -> str:
        """Create a Stripe billing portal session."""
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer.stripe_customer_id,
                return_url=return_url,
            )

            logger.info(
                f"Created billing portal session for customer {customer.stripe_customer_id}"
            )
            return session.url

        except stripe.error.StripeError as exception:
            logger.error(
                f"Failed to create billing portal session for customer {customer.stripe_customer_id}: {exception}"
            )
            raise

    def handle_subscription_created(self, stripe_subscription: dict) -> Subscription:
        """Handle subscription.created webhook event."""
        try:
            customer = Customer.objects.get(
                stripe_customer_id=stripe_subscription["customer"]
            )
            # Get the product ID from the price to find the matching plan
            price_id = stripe_subscription["items"]["data"][0]["price"]["id"]
            price = stripe.Price.retrieve(price_id)
            plan = Plan.objects.get(stripe_product_id=price.product)

            # Get period dates from the first subscription item
            first_item = stripe_subscription["items"]["data"][0]

            subscription = Subscription.objects.create(
                customer=customer,
                plan=plan,
                stripe_subscription_id=stripe_subscription["id"],
                status=stripe_subscription["status"],
                current_period_start=timezone.datetime.fromtimestamp(
                    first_item["current_period_start"], tz=ZoneInfo("UTC")
                ),
                current_period_end=timezone.datetime.fromtimestamp(
                    first_item["current_period_end"], tz=ZoneInfo("UTC")
                ),
                cancel_at_period_end=stripe_subscription["cancel_at_period_end"],
                trial_start=timezone.datetime.fromtimestamp(
                    stripe_subscription["trial_start"], tz=ZoneInfo("UTC")
                )
                if stripe_subscription.get("trial_start")
                else None,
                trial_end=timezone.datetime.fromtimestamp(
                    stripe_subscription["trial_end"], tz=ZoneInfo("UTC")
                )
                if stripe_subscription.get("trial_end")
                else None,
            )

            logger.info(f"Created subscription {subscription.id} from webhook")
            return subscription

        except (Customer.DoesNotExist, Plan.DoesNotExist) as exception:
            logger.error(f"Failed to create subscription from webhook: {exception}")
            raise

    def handle_subscription_updated(self, stripe_subscription: dict) -> Subscription:
        """Handle subscription.updated webhook event."""
        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=stripe_subscription["id"]
            )

            # Get period dates from the first subscription item
            first_item = stripe_subscription["items"]["data"][0]

            subscription.status = stripe_subscription["status"]
            subscription.current_period_start = timezone.datetime.fromtimestamp(
                first_item["current_period_start"], tz=ZoneInfo("UTC")
            )
            subscription.current_period_end = timezone.datetime.fromtimestamp(
                first_item["current_period_end"], tz=ZoneInfo("UTC")
            )
            subscription.cancel_at_period_end = stripe_subscription[
                "cancel_at_period_end"
            ]
            subscription.canceled_at = (
                timezone.datetime.fromtimestamp(
                    stripe_subscription["canceled_at"], tz=ZoneInfo("UTC")
                )
                if stripe_subscription.get("canceled_at")
                else None
            )
            subscription.trial_start = (
                timezone.datetime.fromtimestamp(
                    stripe_subscription["trial_start"], tz=ZoneInfo("UTC")
                )
                if stripe_subscription.get("trial_start")
                else None
            )
            subscription.trial_end = (
                timezone.datetime.fromtimestamp(
                    stripe_subscription["trial_end"], tz=ZoneInfo("UTC")
                )
                if stripe_subscription.get("trial_end")
                else None
            )
            subscription.save()

            logger.info(f"Updated subscription {subscription.id} from webhook")
            return subscription

        except Subscription.DoesNotExist as exception:
            logger.error(f"Failed to update subscription from webhook: {exception}")
            raise

    def handle_subscription_deleted(self, stripe_subscription: dict) -> None:
        """Handle subscription.deleted webhook event."""
        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=stripe_subscription["id"]
            )
            subscription.status = Subscription.Status.CANCELED
            subscription.canceled_at = (
                timezone.datetime.fromtimestamp(
                    stripe_subscription["canceled_at"], tz=ZoneInfo("UTC")
                )
                if stripe_subscription.get("canceled_at")
                else None
            )
            subscription.save()

            logger.info(f"Canceled subscription {subscription.id} from webhook")

        except Subscription.DoesNotExist as exception:
            logger.error(f"Failed to cancel subscription from webhook: {exception}")
            raise

    def handle_payment_intent_succeeded(self, payment_intent: dict) -> Payment:
        """Handle payment_intent.succeeded webhook event."""
        try:
            customer = Customer.objects.get(
                stripe_customer_id=payment_intent["customer"]
            )

            # Try to find associated subscription
            subscription = None
            if payment_intent.get("invoice"):
                try:
                    invoice = stripe.Invoice.retrieve(payment_intent["invoice"])
                    if invoice.get("subscription"):
                        subscription = Subscription.objects.get(
                            stripe_subscription_id=invoice["subscription"]
                        )
                except stripe.error.StripeError, Subscription.DoesNotExist:
                    pass

            payment = Payment.objects.create(
                customer=customer,
                subscription=subscription,
                stripe_payment_intent_id=payment_intent["id"],
                amount=Decimal(payment_intent["amount"]) * STRIPE_CENTS_TO_DOLLARS,
                currency=payment_intent["currency"],
                status=Payment.Status.SUCCEEDED,
                description=payment_intent.get("description", ""),
            )

            logger.info(f"Created payment {payment.id} from webhook")
            return payment

        except Customer.DoesNotExist as exception:
            logger.error(f"Failed to create payment from webhook: {exception}")
            raise

    def get_product_details(self, product_id: str) -> dict:
        """Get product and its default price details from Stripe."""
        try:
            # Get product details
            product = stripe.Product.retrieve(product_id)

            # Get the default price for this product
            prices = stripe.Price.list(product=product_id, active=True, limit=1)
            default_price = prices.data[0] if prices.data else None

            price_details = {}
            if default_price:
                price_details = {
                    "price_id": default_price.id,
                    "amount": Decimal(default_price.unit_amount)
                    * STRIPE_CENTS_TO_DOLLARS
                    if default_price.unit_amount
                    else Decimal("0"),
                    "currency": default_price.currency.upper(),
                    "recurring_interval": default_price.recurring.interval
                    if default_price.recurring
                    else None,
                }

            return {
                "name": product.name,
                "description": product.description or "",
                "price_details": price_details,
                "metadata": product.metadata,
            }
        except stripe.error.StripeError as exception:
            logger.error(f"Failed to retrieve product {product_id}: {exception}")
            return {
                "name": "Unknown Product",
                "description": "",
                "price_details": {
                    "amount": Decimal("0"),
                    "currency": "USD",
                    "recurring_interval": "month",
                },
                "metadata": {},
            }

    def sync_customer_data(self, customer: Customer) -> dict:
        """Sync customer data from Stripe (subscriptions, payments)."""
        try:
            # Get all subscriptions from Stripe (including canceled ones)
            stripe_subscriptions = stripe.Subscription.list(
                customer=customer.stripe_customer_id,
                status="all",  # Include canceled subscriptions
                limit=10,
            )

            # Get payment intents from Stripe
            stripe_payments = stripe.PaymentIntent.list(
                customer=customer.stripe_customer_id, limit=10
            )

            synced_data = {
                "subscriptions_synced": 0,
                "payments_synced": 0,
            }

            # Sync subscriptions
            for stripe_sub in stripe_subscriptions.data:
                try:
                    # Check if subscription already exists
                    existing_sub = Subscription.objects.filter(
                        stripe_subscription_id=stripe_sub["id"]
                    ).first()

                    if not existing_sub:
                        self.handle_subscription_created(stripe_sub)
                        synced_data["subscriptions_synced"] += 1
                    else:
                        self.handle_subscription_updated(stripe_sub)
                        synced_data["subscriptions_synced"] += 1
                except Exception as exception:
                    logger.error(
                        f"Failed to sync subscription {stripe_sub['id']}: {exception}"
                    )

            # Sync payments
            for stripe_payment in stripe_payments.data:
                if stripe_payment.status == Payment.Status.SUCCEEDED:
                    try:
                        # Check if payment already exists
                        existing_payment = Payment.objects.filter(
                            stripe_payment_intent_id=stripe_payment["id"]
                        ).first()

                        if not existing_payment:
                            self.handle_payment_intent_succeeded(stripe_payment)
                            synced_data["payments_synced"] += 1
                    except Exception as exception:
                        logger.error(
                            f"Failed to sync payment {stripe_payment['id']}: {exception}"
                        )

            return synced_data

        except stripe.error.StripeError as exception:
            logger.error(f"Failed to sync customer data: {exception}")
            raise
