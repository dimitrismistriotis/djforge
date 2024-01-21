"""Urls for registering interest in the DJ app."""
from django.urls import path

from .views import manifest

app_name = "dj_content"

urlpatterns = [
    path("/manifest", manifest, name="dj_forge_manifest"),
]
