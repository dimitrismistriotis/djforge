"""Management command to sync data from Stripe."""

from django.core.management.base import BaseCommand

from dj_billing.models import Customer
from dj_billing.services import StripeService


class Command(BaseCommand):
    """Management command to sync customer data from Stripe."""

    help = "Sync subscriptions and payments from Stripe for all customers"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--customer-id",
            type=int,
            help="Sync data for specific customer ID only",
        )

    def handle(self, *args, **options):
        """Handle the command execution."""
        stripe_service = StripeService()

        if options["customer_id"]:
            try:
                customer = Customer.objects.get(id=options["customer_id"])
                customers = [customer]
                self.stdout.write(f"Syncing data for customer: {customer.user.email}")
            except Customer.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f"Customer with ID {options['customer_id']} not found"
                    )
                )
                return
        else:
            customers = Customer.objects.all()
            self.stdout.write(f"Syncing data for {customers.count()} customers")

        total_subscriptions = 0
        total_payments = 0

        for customer in customers:
            try:
                synced_data = stripe_service.sync_customer_data(customer)

                self.stdout.write(
                    f"Customer {customer.user.email}: "
                    f"{synced_data['subscriptions_synced']} subscriptions, "
                    f"{synced_data['payments_synced']} payments synced"
                )

                total_subscriptions += synced_data["subscriptions_synced"]
                total_payments += synced_data["payments_synced"]

            except Exception as exception:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed to sync data for customer {customer.user.email}: {exception}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Sync complete! Total: {total_subscriptions} subscriptions, "
                f"{total_payments} payments synced"
            )
        )
