from django.urls import path

from . import views

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from quiz.models import Question

info_dict = {
    'queryset': Question.objects.all(),
}

sitemap_dict = {
    'sitemaps': {'question': GenericSitemap(info_dict, priority=0.8)}
}


urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<slug:slug>/<int:level>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<slug:slug_quiz>/<int:level_quiz>/<slug:slug_lection>/<int:id_question>/',views.question_detail, name='question_detail'),

    # htmx
    path('hx/quiz/search-quizzes/', views.search_quizzes, name='search_quizzes'),
    path('hx/quiz/<slug:slug_quiz>/<int:level_quiz>/<slug:slug_lection>/<int:id_question>/check-answer/', views.check_answer, name='check_answer'),
    path('hx/quiz/<slug:slug_quiz>/<int:level_quiz>/<slug:slug_lection>/<int:id_question>/update-progress-bar/', views.update_progress_bar, name='update_progress_bar'),
    
    # htmx - question translation
    path('hx/question/get-translation-modal/<int:id_question>/', views.get_question_translation_modal, name='quiz_get_translation_modal'),
    path('hx/question/translate/<int:id_question>/<int:id_language>/', views.translate_question_text, name='quiz_translate_question_text'),
    
    # sitemaps
    path('questions/sitemap.xml', sitemap, sitemap_dict, name='django.contrib.sitemaps.views.sitemap'),

]
