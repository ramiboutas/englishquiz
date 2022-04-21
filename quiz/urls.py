from django.urls import path

from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<slug:slug>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<slug:slug_quiz>/<slug:slug_lection>/<int:id_question>/',views.question_detail, name='question_detail'),
]
