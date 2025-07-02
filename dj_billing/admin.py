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

    list_display = ["name", "plan_type", "price", "max_developers", "is_active"]
    list_filter = ["plan_type", "is_active"]
    search_fields = ["name", "stripe_price_id"]
    readonly_fields = ["created_at", "updated_at"]


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
    list_filter = ["status", "plan__plan_type", "created_at"]
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
