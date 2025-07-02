"""Management command to set up default billing plans."""

from django.conf import settings
from django.core.management.base import BaseCommand

from dj_billing.models import Plan


class Command(BaseCommand):
    """Management command to create default billing plans."""

    help = "Create default billing plans from settings"

    def handle(self, *args, **options):
        """Handle the command execution."""
        plans_data = [
            {
                "name": "Starter",
                "plan_type": "starter",
                "stripe_price_id": settings.STRIPE_PRICE_ID_STARTER,
                "price": 29.00,
                "max_developers": 1,
                "support_months": 6,
            },
            {
                "name": "Company",
                "plan_type": "company",
                "stripe_price_id": settings.STRIPE_PRICE_ID_COMPANY,
                "price": 99.00,
                "max_developers": 10,
                "support_months": 24,
            },
            {
                "name": "Enterprise",
                "plan_type": "enterprise",
                "stripe_price_id": settings.STRIPE_PRICE_ID_ENTERPRISE,
                "price": 499.00,
                "max_developers": 100,
                "support_months": 36,
            },
        ]

        for plan_data in plans_data:
            if not plan_data["stripe_price_id"]:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping {plan_data['name']} plan - no Stripe price ID configured"
                    )
                )
                continue

            plan, created = Plan.objects.get_or_create(
                plan_type=plan_data["plan_type"],
                defaults=plan_data,
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created plan: {plan.name}")
                )
            else:
                # Update existing plan with new data
                for field, value in plan_data.items():
                    setattr(plan, field, value)
                plan.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Updated plan: {plan.name}")
                )

        self.stdout.write(
            self.style.SUCCESS("Successfully set up billing plans")
        )