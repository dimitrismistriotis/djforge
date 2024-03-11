"""Urls for registering interest in the DJ app."""

from django.urls import path

from .views import dashboard

app_name = "dj_dashboard"


urlpatterns = (path("", dashboard, name="dashboard"),)
