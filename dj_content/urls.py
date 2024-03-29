"""Urls for content the DJ app."""

from django.urls import path

from .views import about_us
from .views import health

app_name = "dj_content"

urlpatterns = [
    path("about_us", about_us, name="about-us"),
    path("health", health, name="health"),
]
