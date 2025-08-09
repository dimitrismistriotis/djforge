"""Urls for content the DJ app."""

from django.urls import path

from .views import about_us
from .views import cookies_policy
from .views import health
from .views import license

app_name = "dj_content"

urlpatterns = [
    path(
        "about_us",
        about_us,
        name="about-us",
    ),
    path(
        "cookies_policy",
        cookies_policy,
        name="cookies-policy",
    ),
    path(
        "health",
        health,
        name="health",
    ),
    path(
        "license",
        license,
        name="license",
    ),
]
