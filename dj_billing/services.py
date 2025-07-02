"""Stripe service module for handling Stripe API operations."""

import logging
from decimal import Decimal

import stripe

from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Customer
from .models import Payment
from .models import Plan
from .models import Subscription

logger = logging.getLogger(__name__)

User = get_user_model()


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

            logger.info(f"Created Stripe customer {stripe_customer.id} for user {user.email}")
            return customer

        except stripe.error.StripeError as exception:
            logger.error(f"Failed to create Stripe customer for user {user.email}: {exception}")
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
            session_data = {
                "customer": customer.stripe_customer_id,
                "payment_method_types": ["card"],
                "line_items": [
                    {
                        "price": plan.stripe_price_id,
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
            plan = Plan.objects.get(
                stripe_price_id=stripe_subscription["items"]["data"][0]["price"]["id"]
            )

            subscription = Subscription.objects.create(
                customer=customer,
                plan=plan,
                stripe_subscription_id=stripe_subscription["id"],
                status=stripe_subscription["status"],
                current_period_start=stripe_subscription["current_period_start"],
                current_period_end=stripe_subscription["current_period_end"],
                cancel_at_period_end=stripe_subscription["cancel_at_period_end"],
                trial_start=stripe_subscription.get("trial_start"),
                trial_end=stripe_subscription.get("trial_end"),
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

            subscription.status = stripe_subscription["status"]
            subscription.current_period_start = stripe_subscription["current_period_start"]
            subscription.current_period_end = stripe_subscription["current_period_end"]
            subscription.cancel_at_period_end = stripe_subscription["cancel_at_period_end"]
            subscription.canceled_at = stripe_subscription.get("canceled_at")
            subscription.trial_start = stripe_subscription.get("trial_start")
            subscription.trial_end = stripe_subscription.get("trial_end")
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
            subscription.status = "canceled"
            subscription.canceled_at = stripe_subscription.get("canceled_at")
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
                except (stripe.error.StripeError, Subscription.DoesNotExist):
                    pass

            payment = Payment.objects.create(
                customer=customer,
                subscription=subscription,
                stripe_payment_intent_id=payment_intent["id"],
                amount=Decimal(payment_intent["amount"]) / 100,  # Convert from cents
                currency=payment_intent["currency"],
                status="succeeded",
                description=payment_intent.get("description", ""),
            )

            logger.info(f"Created payment {payment.id} from webhook")
            return payment

        except Customer.DoesNotExist as exception:
            logger.error(f"Failed to create payment from webhook: {exception}")
            raise

    def cancel_subscription(self, subscription: Subscription) -> None:
        """Cancel a subscription at the end of the current period."""
        try:
            stripe.Subscription.modify(
                subscription.stripe_subscription_id,
                cancel_at_period_end=True,
            )

            subscription.cancel_at_period_end = True
            subscription.save()

            logger.info(f"Canceled subscription {subscription.id} at period end")

        except stripe.error.StripeError as exception:
            logger.error(f"Failed to cancel subscription {subscription.id}: {exception}")
            raise

    def reactivate_subscription(self, subscription: Subscription) -> None:
        """Reactivate a canceled subscription."""
        try:
            stripe.Subscription.modify(
                subscription.stripe_subscription_id,
                cancel_at_period_end=False,
            )

            subscription.cancel_at_period_end = False
            subscription.save()

            logger.info(f"Reactivated subscription {subscription.id}")

        except stripe.error.StripeError as exception:
            logger.error(f"Failed to reactivate subscription {subscription.id}: {exception}")
            raise