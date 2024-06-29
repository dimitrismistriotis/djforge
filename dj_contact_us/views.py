"""Contact Us views."""
import logging

from django.contrib import messages
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from dj_emails.dispatchers import contact_us_email_dispatcher
from dj_emails.exceptions import EmailDispatcherException

from .forms import ContactUsEntryForm

# from django.core.mail import send_mail




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

            try:
                contact_us_email_dispatcher(
                    name=contact_form.name,
                    email=contact_form.email,
                    message=contact_form.message,
                )
            except EmailDispatcherException as email_exception:
                # Inform for the error and proceed, no need to break if email fails.
                logger.error(
                    f"Error sending email: {email_exception}",
                    extra={"contact_form": contact_form},
                )

            messages.success(request, "Your message has been sent successfully.")

            return redirect("dj_contact_us:contact-us")
    else:
        form = ContactUsEntryForm()
    return render(request, "dj_contact_us/contact.html", {"form": form})
