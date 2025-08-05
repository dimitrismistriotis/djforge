"""URL configuration for dj_billing app."""

from django.urls import path

from . import views

app_name = "dj_billing"

urlpatterns = [
    path("", views.BillingView.as_view(), name="pricing"),
    path(
        "checkout/",
        views.CreateCheckoutSessionView.as_view(),
        name="create_checkout_session",
    ),
    path("portal/", views.BillingPortalView.as_view(), name="billing_portal"),
    path("success/", views.SuccessView.as_view(), name="success"),
    path("webhooks/stripe/", views.stripe_webhook, name="stripe_webhook"),
]
