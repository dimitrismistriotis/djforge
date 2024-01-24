"""Urls for registering interest in the DJ app."""
from django.urls import path

from .views import about_us

app_name = "dj_content"

urlpatterns = [
    path("about_us", about_us, name="about-us"),
]
