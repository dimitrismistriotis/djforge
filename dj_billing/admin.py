"""Admin configuration for dj_billing app."""

from django.contrib import admin

from .models import Customer
from .models import Payment
from .models import Plan
from .models import Subscription


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin configuration for Customer model."""

    list_display = ["user", "stripe_customer_id", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__email", "stripe_customer_id"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Admin configuration for Plan model."""

    list_display = ["stripe_name_display", "stripe_price_display", "order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["stripe_product_id"]
    list_editable = ["order"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "stripe_name_display",
        "stripe_price_display",
    ]

    def stripe_name_display(self, obj):
        """Display Stripe product name."""
        try:
            stripe_details = obj.get_stripe_details()
            return stripe_details.get("name", "Unknown Plan")
        except Exception as e:
            return f"Error: {str(e)[:30]}"

    stripe_name_display.short_description = "Product Name (from Stripe)"

    def stripe_price_display(self, obj):
        """Display current Stripe price."""
        try:
            stripe_details = obj.get_stripe_details()
            price_details = stripe_details.get("price_details", {})
            if price_details and price_details.get("amount"):
                currency_symbol = (
                    "€" if price_details["currency"].upper() == "EUR" else "$"
                )
                return f"{price_details['amount']}{currency_symbol}/{price_details['recurring_interval']}"
            return "No price found"
        except Exception as e:
            return f"Error: {str(e)[:50]}"

    stripe_price_display.short_description = "Current Stripe Price"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin configuration for Subscription model."""

    list_display = [
        "customer",
        "plan",
        "status",
        "current_period_start",
        "current_period_end",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["customer__user__email", "stripe_subscription_id"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "current_period_start"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin configuration for Payment model."""

    list_display = ["customer", "amount", "currency", "status", "created_at"]
    list_filter = ["status", "currency", "created_at"]
    search_fields = ["customer__user__email", "stripe_payment_intent_id"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
