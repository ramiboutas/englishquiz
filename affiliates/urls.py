from __future__ import annotations

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from affiliates.models import Book

info_dict = {
    "queryset": Book.objects.all(),
}

sitemap_dict = {"sitemaps": {"question": GenericSitemap(info_dict, priority=0.8)}}


urlpatterns = [
    path("list/", views.quiz_list, name="book_list"),
    path("<slug:slug>/", views.quiz_detail, name="book_detail"),

    # htmx
    path("hx/search-books/", views.search_quizzes, name="search_books"),
    
    # htmx - question translation
    path(
        "hx/question/translate/<int:id_question>/<int:id_language>/",
        views.translate_question_text,
        name="quiz_translate_question_text",
    ),
    
    
    # sitemaps
    path(
        "books/sitemap.xml",
        sitemap,
        sitemap_dict,
        name="django.contrib.sitemaps.views.sitemap",
    ),

]
