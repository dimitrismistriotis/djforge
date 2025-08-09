"""Urls for Contact Us of the DJ app."""

from django.urls import path

from .views import contact_view

app_name = "dj_contact_us"

urlpatterns = [
    path(
        "",
        contact_view,
        name="contact-us",
    ),
]
