from __future__ import annotations

from django.urls import path

from .views import contact_view, flexpage_detail_view, home_view

urlpatterns = [
    path("", home_view, name="pages_home"),
    path("contact/", contact_view, name="pages_contact"),
    # path("hx/contact/thanks/", contact_thanks_view, name="pages_contact"),
    # This path goes at the end
    path("<slug:slug>/", flexpage_detail_view, name="pages_flexpage"),
]
