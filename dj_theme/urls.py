"""Urls for Theme in the DJ app."""

from django.conf import settings
from django.urls import path

from .views import dashboard_template
from .views import logging_demo
from .views import messages_demo

app_name = "dj_theme"


#
# Theme URLs should be available only in DEBUG mode / development environments.
#
urlpatterns = (
    [
        path(
            "messages",
            messages_demo,
            name="messages_demo",
        ),
        path(
            "logging",
            logging_demo,
            name="logging_demo",
        ),
        path("dashboard", dashboard_template, name="dashboard"),
    ]
    if getattr(settings, "DEBUG", False)
    else []
)
