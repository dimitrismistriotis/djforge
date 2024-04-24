"""Contact Us views."""
import logging

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpRequest
# from django.core.mail import send_mail


from .forms import ContactUsEntryForm


def contact_view(request: HttpRequest) -> HttpResponse:
    """Contact Us view."""
    logger = logging.getLogger(__name__)

    if request.method == "POST":
        form = ContactUsEntryForm(request.POST)
        if form.is_valid():
            contact_form = form.save()
            logger.info(
                "New Contact Form Submission", extra={"contact_form": contact_form}
            )
            # email_subject = "New Contact Form Submission"
            # email_message = f"Name: {contact_form.name}\nEmail: {contact_form.email}\nMessage: {contact_form.message}"
            # admin_email = "admin@example.com"  # Replace with your admin email
            # send_mail(
            # email_subject,
            # email_message,
            # "noreply@example.com",
            # [contact_form.email, admin_email],
            # )
            messages.success(request, "Your message has been sent successfully.")

            return redirect("contact")
    else:
        form = ContactUsEntryForm()
    return render(request, "contact.html", {"form": form})
