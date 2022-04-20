from django.urls import path

from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<slug:slug>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:id_quiz>/lection/<int:id_lection>/question/<int:id_question>/',views.question_detail, name='question_detail'),
]
