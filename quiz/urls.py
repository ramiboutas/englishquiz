from __future__ import annotations

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from quiz.models import Question

from . import views

info_dict = {
    "queryset": Question.objects.all(),
}

sitemap_dict = {"sitemaps": {"question": GenericSitemap(info_dict, priority=0.8)}}


urlpatterns = [
    path("list/", views.quiz_list, name="quiz_list"),
    path("<slug:slug>/<int:level>/", views.quiz_detail, name="quiz_detail"),
    path(
        "<slug:slug_quiz>/<int:level_quiz>/<slug:slug_lection>/<int:id_question>/",
        views.question_detail,
        name="question_detail",
    ),
    # htmx
    path("hx/search-quizzes/", views.search_quizzes, name="search_quizzes"),
    path(
        "hx/<slug:slug_quiz>/<int:level_quiz>/<slug:slug_lection>/<int:id_question>/check-answer/",
        views.check_answer,
        name="check_answer",
    ),
    path(
        "hx/<slug:slug_quiz>/<int:level_quiz>/<slug:slug_lection>/<int:id_question>/update-progress-bar/",
        views.update_progress_bar,
        name="update_progress_bar",
    ),
    # htmx - question translation
    path(
        "hx/question/translate/<int:id_question>/<int:id_language>/",
        views.translate_question_text,
        name="quiz_translate_question_text",
    ),
    # sitemaps
    path(
        "questions/sitemap.xml",
        sitemap,
        sitemap_dict,
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # not used, used Bootstrap Bundle JS instead
    path(
        "hx/question/get-translation-modal/<int:id_question>/",
        views.get_question_translation_modal,
        name="quiz_get_translation_modal",
    ),
    path(
        "hx/question/remove-translation-modal/<int:id_question>/",
        views.remove_question_translation_modal,
        name="quiz_remove_translation_modal",
    ),
]
