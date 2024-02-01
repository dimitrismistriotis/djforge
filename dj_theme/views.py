"""Views for dj_theme app."""
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib import messages


def messages_demo(request: HttpRequest) -> HttpResponse:
    """Display different messages to demonstrate their UI.

    Reference: https://docs.djangoproject.com/en/5.0/ref/contrib/messages/
    """
    messages.debug(request, "This is a DEBUG message.")
    messages.info(request, "This is an INFO message.")
    messages.success(request, "This is a SUCCESS message.")
    messages.warning(request, "This is a WARNING message.")
    messages.error(request, "This is an ERROR message.")

    return render(request, "dj_theme/demo_display_messages.html")
