from django.urls import path

from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<slug:slug>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<slug:slug_quiz>/<slug:slug_lection>/<int:id_question>/',views.question_detail, name='question_detail'),

    # htmx
    path('hx/quiz/<slug:slug_quiz>/<slug:slug_lection>/<int:id_question>/check-answer/',views.check_answer, name='check_answer'),
    path('hx/quiz/<slug:slug_quiz>/<slug:slug_lection>/<int:id_question>/update-progress-bar/',views.update_progress_bar, name='update_progress_bar'),

]
