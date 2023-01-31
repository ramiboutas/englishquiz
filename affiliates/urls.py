from __future__ import annotations

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from affiliates.models import Book

info_dict = {
    "queryset": Book.objects.all(),
}

sitemap_dict = {"sitemaps": {"books": GenericSitemap(info_dict, priority=0.8)}}


urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("book/<slug:slug>/", views.book_detail, name="book_detail"),

    # htmx
    path("hx/search-books/", views.search_books, name="search_books"),
    
    # sitemaps
    path(
        "books/sitemap.xml",
        sitemap,
        sitemap_dict,
        name="django.contrib.sitemaps.views.sitemap",
    ),

]
