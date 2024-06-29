"""Urls for PoCs of the DJ app."""

from django.urls import path

from .views import admin_only_display
from .views import map_and_postcode_analysis

app_name = "dj_pocs"

urlpatterns = [
    path("admin_view", admin_only_display, name="admin_only_display"),
    path("map", map_and_postcode_analysis, name="map_and_postcode_analysis"),
]
