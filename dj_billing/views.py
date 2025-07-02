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
            messages.info(request, "Stripe API keys not configured. This is a demo of the billing interface.")
        
        subscriptions = Subscription.objects.for_user(request.user).order_by("-created_at") if customer else []
        active_subscription = subscriptions.filter(status__in=["active", "trialing"]).first() if subscriptions else None
        
        plans = Plan.objects.active().order_by("price")
        
        context = {
            "customer": customer,
            "active_subscription": active_subscription,
            "subscriptions": subscriptions,
            "plans": plans,
            "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
            "stripe_configured": bool(settings.STRIPE_SECRET_KEY and settings.STRIPE_PUBLISHABLE_KEY),
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
            return redirect("dj_billing:billing")
        
        plan = get_object_or_404(Plan, id=plan_id, is_active=True)
        
        stripe_service = StripeService()
        customer = stripe_service.get_or_create_customer(request.user)
        
        # Check if user already has an active subscription
        active_subscription = Subscription.objects.for_user(request.user).filter(
            status__in=["active", "trialing"]
        ).first()
        
        if active_subscription:
            messages.error(request, "You already have an active subscription.")
            return redirect("dj_billing:billing")
        
        try:
            success_url = request.build_absolute_uri(reverse("dj_billing:success"))
            cancel_url = request.build_absolute_uri(reverse("dj_billing:billing"))
            
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
            messages.error(request, "There was an error processing your request. Please try again.")
            return redirect("dj_billing:billing")


@method_decorator(login_required, name="dispatch")
class BillingPortalView(View):
    """Redirect to Stripe Customer Portal."""

    def post(self, request):
        """Create billing portal session and redirect."""
        stripe_service = StripeService()
        
        try:
            customer = stripe_service.get_or_create_customer(request.user)
            return_url = request.build_absolute_uri(reverse("dj_billing:billing"))
            
            portal_url = stripe_service.create_billing_portal_session(
                customer=customer,
                return_url=return_url,
            )
            
            return redirect(portal_url)
            
        except stripe.error.StripeError as exception:
            logger.error(f"Stripe portal error: {exception}")
            messages.error(request, "There was an error accessing the billing portal. Please try again.")
            return redirect("dj_billing:billing")


@method_decorator(login_required, name="dispatch")
class SuccessView(View):
    """Payment success page."""

    def get(self, request):
        """Display payment success page."""
        messages.success(request, "Payment successful! Your subscription is now active.")
        return redirect("dj_billing:billing")


@method_decorator(login_required, name="dispatch")
class CancelSubscriptionView(View):
    """Cancel subscription view."""

    def post(self, request):
        """Cancel user's active subscription."""
        subscription_id = request.POST.get("subscription_id")
        
        if not subscription_id:
            messages.error(request, "Invalid subscription.")
            return redirect("dj_billing:billing")
        
        subscription = get_object_or_404(
            Subscription,
            id=subscription_id,
            customer__user=request.user,
            status__in=["active", "trialing"],
        )
        
        stripe_service = StripeService()
        
        try:
            stripe_service.cancel_subscription(subscription)
            messages.success(
                request,
                "Your subscription has been canceled and will end at the current billing period."
            )
            
        except stripe.error.StripeError as exception:
            logger.error(f"Stripe cancel error: {exception}")
            messages.error(request, "There was an error canceling your subscription. Please try again.")
        
        return redirect("dj_billing:billing")


@method_decorator(login_required, name="dispatch")
class ReactivateSubscriptionView(View):
    """Reactivate subscription view."""

    def post(self, request):
        """Reactivate user's canceled subscription."""
        subscription_id = request.POST.get("subscription_id")
        
        if not subscription_id:
            messages.error(request, "Invalid subscription.")
            return redirect("dj_billing:billing")
        
        subscription = get_object_or_404(
            Subscription,
            id=subscription_id,
            customer__user=request.user,
            cancel_at_period_end=True,
        )
        
        stripe_service = StripeService()
        
        try:
            stripe_service.reactivate_subscription(subscription)
            messages.success(request, "Your subscription has been reactivated.")
            
        except stripe.error.StripeError as exception:
            logger.error(f"Stripe reactivate error: {exception}")
            messages.error(request, "There was an error reactivating your subscription. Please try again.")
        
        return redirect("dj_billing:billing")


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
