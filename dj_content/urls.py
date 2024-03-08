"""Urls for registering interest in the DJ app."""

from django.urls import path
from django.conf import settings

from .views import about_us
from .views import dashboard_template

app_name = "dj_content"

urlpatterns = [
    path("about_us", about_us, name="about-us"),
]

if getattr(settings, "DEBUG", False):
    urlpatterns.append(path("dashboard", dashboard_template, name="dashboard"))
