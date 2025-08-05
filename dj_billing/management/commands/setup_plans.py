"""Management command to set up default billing plans."""

from django.conf import settings
from django.core.management.base import BaseCommand

from dj_billing.models import Plan


class Command(BaseCommand):
    """Management command to create default billing plans."""

    help = "Create default billing plans using Stripe product IDs"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--product-id",
            type=str,
            help="Stripe product ID to create a plan for",
        )
        parser.add_argument(
            "--order",
            type=int,
            default=0,
            help="Display order for the plan",
        )

    def handle(self, *args, **options):
        """Handle the command execution."""
        if options["product_id"]:
            # Create a single plan with the provided product ID
            self.create_plan(options["product_id"], options["order"])
        else:
            # Create default plans from environment variables (if available)
            self.create_default_plans()

    def create_plan(self, product_id: str, order: int = 0):
        """Create a plan with the given Stripe product ID."""
        try:
            plan, created = Plan.objects.get_or_create(
                stripe_product_id=product_id,
                defaults={"order": order, "is_active": True},
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created plan: {plan} (Product: {product_id})")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Plan already exists: {plan} (Product: {product_id})"
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Failed to create plan for product {product_id}: {e}")
            )

    def create_default_plans(self):
        """Create default plans from environment variables."""
        default_products = [
            ("STRIPE_PRODUCT_ID_STARTER", 1),
            ("STRIPE_PRODUCT_ID_COMPANY", 2),
            ("STRIPE_PRODUCT_ID_ENTERPRISE", 3),
        ]

        plans_created = 0
        for env_var, order in default_products:
            product_id = getattr(settings, env_var, None)
            if product_id:
                self.create_plan(product_id, order)
                plans_created += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f"Environment variable {env_var} not set")
                )

        if plans_created == 0:
            self.stdout.write(
                self.style.WARNING(
                    "No plans created. Use --product-id to create individual plans, "
                    "or set STRIPE_PRODUCT_ID_* environment variables."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created {plans_created} plans")
            )
