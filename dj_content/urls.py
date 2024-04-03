"""Urls for content the DJ app."""

from django.urls import path

from .views import about_us
from .views import health
from .views import license

app_name = "dj_content"

urlpatterns = [
    path("about_us", about_us, name="about-us"),
    path("health", health, name="health"),
    path("license", license, name="license"),
]
