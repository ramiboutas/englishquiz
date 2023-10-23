from __future__ import annotations

from django.urls import path

from .views import home_view, AdsView, flexpage_detail_view, contact_view

urlpatterns = [
    path("", home_view, name="core_home"),
    path("contact/", contact_view, name="core_contact"),
    path("p/<slug:slug>/", flexpage_detail_view, name="core_flexpage"),
    path("ads.txt", AdsView.as_view()),
]
