from __future__ import annotations

from django.urls import path

from .views import contact_view
from .views import flexpage_detail_view
from .views import home_view

urlpatterns = [
    path("", home_view, name="pages_home"),
    path("contact/", contact_view, name="pages_contact"),
    path("p/<slug:slug>/", flexpage_detail_view, name="pages_flexpage"),
]
