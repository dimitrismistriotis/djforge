"""Urls for registering interest in the DJ app."""
from django.urls import path

from .views import RegisterInterestView

app_name = "dj_register_interest"

urlpatterns = [
    path("", RegisterInterestView.as_view(), name="register_interest"),
]
