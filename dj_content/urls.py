"""Urls for registering interest in the DJ app."""
from django.urls import path

from .views import about_us
from .views import dashboard_template

app_name = "dj_content"

urlpatterns = [
    path("about_us", about_us, name="about-us"),
    path("dashboard", dashboard_template, name="dashboard-template"),
]
