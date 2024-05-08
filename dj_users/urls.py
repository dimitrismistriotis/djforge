"""Urls for the DJ users."""

from django.urls import path

from .views import admin_account, user_account

app_name = "dj_users"

urlpatterns = [
    path("admin_account", admin_account, name="admin_account"),
    path("user_account", user_account, name="user_account"),
]
