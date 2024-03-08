"""Views for dj_theme app."""

import logging

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
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


def logging_demo(_request: HttpRequest) -> JsonResponse:
    """Display different log levels to demonstrate their UI.

    Reference: https://docs.djangoproject.com/en/5.0/topics/logging/

    Can be called with:

    ```shell
    poetry run http localhost:8000/theme/logging
    ```
    """
    logger = logging.getLogger(__name__)
    logger.debug("This is a DEBUG log message.")
    logger.info("This is an INFO log message.")
    logger.warning("This is a WARNING log message.")
    logger.error("This is an ERROR log message.")
    logger.critical("This is a CRITICAL log message.")

    return JsonResponse({"status": "success"})


def dashboard_template(request: HttpRequest) -> HttpResponse:
    """Return a Dashboard page, to use in development while integrating."""
    return render(request, "dj_content/dashboard.html")
