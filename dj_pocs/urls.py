"""Urls for PoCs of the DJ app."""

from django.urls import path

from .views import map_and_postcode_analysis

app_name = "dj_pocs"

urlpatterns = [
    path("map", map_and_postcode_analysis, name="map_and_postcode_analysis"),
]
