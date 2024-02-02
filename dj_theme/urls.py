"""Urls for registering interest in the DJ app."""
from django.urls import path

from .views import messages_demo
from .views import logging_demo

app_name = "dj_theme"

urlpatterns = [
    path("messages", messages_demo, name="messages_demo"),
    path("logging", logging_demo, name="logging_demo"),
]
