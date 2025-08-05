"""Views for dj_billing app."""

import logging
from http import HTTPStatus

import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Plan
from .models import Subscription
from .services import StripeService

logger = logging.getLogger(__name__)


@method_decorator(login_required, name="dispatch")
class BillingView(View):
    """Main billing page view."""

    def get(self, request):
        """Display billing information and subscription status."""
        customer = None

        # Only try to create/get customer if Stripe keys are configured
        if settings.STRIPE_SECRET_KEY and settings.STRIPE_PUBLISHABLE_KEY:
            try:
                stripe_service = StripeService()
                customer = stripe_service.get_or_create_customer(request.user)
            except stripe.error.StripeError as exception:
                logger.error(f"Stripe error: {exception}")
                messages.warning(request, "Billing service temporarily unavailable.")
        else:
            messages.info(
                request,
                "Stripe API keys not configured. This is a demo of the billing interface.",
            )

        subscriptions = (
            Subscription.objects.for_user(request.user).order_by("-created_at")
            if customer
            else []
        )
        active_subscription = (
            subscriptions.filter(status__in=["active", "trialing"]).first()
            if subscriptions
            else None
        )

        # Auto-sync for local development when webhooks don't work
        if settings.DEBUG and settings.STRIPE_AUTO_SYNC_LOCAL and customer:
            should_sync = False
            sync_reason = ""

            # Case 1: No subscriptions found but customer exists
            if not subscriptions.exists():
                should_sync = True
                sync_reason = "no subscriptions found"

            # Case 2: Check if active subscriptions might be stale (canceled in Stripe)
            elif active_subscription:
                # If there's an active subscription, occasionally check if it's still active in Stripe
                # We'll do this on every page load in local dev since webhooks don't work
                should_sync = True
                sync_reason = "verifying active subscription status"

            if should_sync:
                try:
                    sync_result = stripe_service.sync_customer_data(customer)
                    if sync_result["subscriptions_synced"] > 0:
                        logger.info(f"Auto-synced ({sync_reason}): {sync_result}")
                        # Refresh data after sync
                        subscriptions = Subscription.objects.for_user(
                            request.user
                        ).order_by("-created_at")
                        active_subscription = subscriptions.filter(
                            status__in=["active", "trialing"]
                        ).first()
                except Exception as exception:
                    logger.error(
                        f"Failed to auto-sync subscriptions ({sync_reason}): {exception}"
                    )

        plans = Plan.objects.active().order_by("order", "created_at")

        # Enrich plans with current Stripe prices
        plans_with_stripe_prices = []
        stripe_service = StripeService() if settings.STRIPE_SECRET_KEY else None

        for plan in plans:
            plan_dict = {
                "plan": plan,
                "stripe_price": None,
            }

            if stripe_service:
                try:
                    stripe_details = plan.get_stripe_details()
                    plan_dict["stripe_price"] = stripe_details.get("price_details", {})
                    plan_dict["stripe_details"] = stripe_details
                except Exception as exception:
                    logger.error(
                        f"Failed to get Stripe details for plan {plan.id}: {exception}"
                    )

            plans_with_stripe_prices.append(plan_dict)

        context = {
            "customer": customer,
            "active_subscription": active_subscription,
            "subscriptions": subscriptions,
            "plans": plans,
            "plans_with_stripe_prices": plans_with_stripe_prices,
            "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
            "stripe_configured": bool(
                settings.STRIPE_SECRET_KEY and settings.STRIPE_PUBLISHABLE_KEY
            ),
        }

        return render(request, "dj_billing/billing.html", context)


@method_decorator(login_required, name="dispatch")
class CreateCheckoutSessionView(View):
    """Create Stripe Checkout Session."""

    def post(self, request):
        """Create checkout session and redirect to Stripe Checkout."""
        plan_id = request.POST.get("plan_id")

        if not plan_id:
            messages.error(request, "Please select a plan.")
            return redirect("dj_billing:pricing")

        plan = get_object_or_404(Plan, id=plan_id, is_active=True)

        stripe_service = StripeService()
        customer = stripe_service.get_or_create_customer(request.user)

        # Check if user already has an active subscription
        active_subscription = (
            Subscription.objects.for_user(request.user)
            .filter(status__in=["active", "trialing"])
            .first()
        )

        if active_subscription:
            messages.error(request, "You already have an active subscription.")
            return redirect("dj_billing:pricing")

        try:
            success_url = request.build_absolute_uri(reverse("dj_billing:success"))
            cancel_url = request.build_absolute_uri(reverse("dj_billing:pricing"))

            checkout_url = stripe_service.create_checkout_session(
                customer=customer,
                plan=plan,
                success_url=success_url,
                cancel_url=cancel_url,
                trial_period_days=7,  # 7-day trial
            )

            return redirect(checkout_url)

        except stripe.error.StripeError as exception:
            logger.error(f"Stripe checkout error: {exception}")
            messages.error(
                request, "There was an error processing your request. Please try again."
            )
            return redirect("dj_billing:pricing")


@method_decorator(login_required, name="dispatch")
class BillingPortalView(View):
    """Redirect to Stripe Customer Portal."""

    def post(self, request):
        """Create billing portal session and redirect."""
        stripe_service = StripeService()

        try:
            customer = stripe_service.get_or_create_customer(request.user)
            return_url = request.build_absolute_uri(reverse("dj_billing:pricing"))

            portal_url = stripe_service.create_billing_portal_session(
                customer=customer,
                return_url=return_url,
            )

            return redirect(portal_url)

        except stripe.error.StripeError as exception:
            logger.error(f"Stripe portal error: {exception}")
            messages.error(
                request,
                "There was an error accessing the billing portal. Please try again.",
            )
            return redirect("dj_billing:pricing")


@method_decorator(login_required, name="dispatch")
class SuccessView(View):
    """Payment success page."""

    def get(self, request):
        """Display payment success page."""
        # Auto-sync data from Stripe after successful checkout (for local development)
        if settings.DEBUG and settings.STRIPE_AUTO_SYNC_LOCAL:
            try:
                stripe_service = StripeService()
                customer = stripe_service.get_or_create_customer(request.user)
                sync_result = stripe_service.sync_customer_data(customer)
                logger.info(f"Auto-synced after checkout: {sync_result}")
            except Exception as exception:
                logger.error(f"Failed to auto-sync after checkout: {exception}")

        messages.success(
            request, "Payment successful! Your subscription is now active."
        )
        return redirect("dj_billing:pricing")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhook events."""
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if not endpoint_secret:
        logger.warning("Stripe webhook secret not configured")
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        logger.error("Invalid payload in Stripe webhook")
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature in Stripe webhook")
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)

    logger.info(f"Received Stripe webhook event: {event['type']}")

    stripe_service = StripeService()

    try:
        if event["type"] == "customer.subscription.created":
            stripe_service.handle_subscription_created(event["data"]["object"])

        elif event["type"] == "customer.subscription.updated":
            stripe_service.handle_subscription_updated(event["data"]["object"])

        elif event["type"] == "customer.subscription.deleted":
            stripe_service.handle_subscription_deleted(event["data"]["object"])

        elif event["type"] == "payment_intent.succeeded":
            stripe_service.handle_payment_intent_succeeded(event["data"]["object"])

        else:
            logger.info(f"Unhandled webhook event type: {event['type']}")

    except Exception as exception:
        logger.error(f"Error processing webhook event {event['type']}: {exception}")
        return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return HttpResponse(status=HTTPStatus.OK)
