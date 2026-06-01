"""URL configuration for dj_surveys app."""

from django.conf import settings
from django.urls import path

from dj_surveys import views

app_name = "dj_surveys"

urlpatterns = [
    path(
        "submit-vote/",
        views.submit_survey_vote,
        name="submit_vote",
    ),
    path(
        "skip/<int:survey_id>/",
        views.skip_survey,
        name="skip_survey",
    ),
]

if settings.DEBUG:
    from dj_surveys.preview.urls import urlpatterns as preview_urlpatterns

    urlpatterns += preview_urlpatterns
