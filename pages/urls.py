from django.urls import path

from .views import flexpage_detail_view, home_view, contact_view

urlpatterns = [
    path("", home_view, name="pages_home"),
    
    path("contact/", contact_view, name="pages_contact"),
    path("<slug:slug>/", flexpage_detail_view, name="pages_flexpage"),
    
]