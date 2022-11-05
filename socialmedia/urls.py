from __future__ import annotations

from django.urls import path

from .views import linkedin_view
from .views import telegram_view
from .views import twitter_view

urlpatterns = [
    path("telegram/", telegram_view, name="socialmedia_telegram"),
    path("linkedin/", linkedin_view, name="socialmedia_linkedin"),
    path("twitter/", twitter_view, name="socialmedia_twitter"),
]
