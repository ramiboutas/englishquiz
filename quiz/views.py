from __future__ import annotations

import random

import deepl
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django_htmx.http import trigger_client_event

from .models import Answer
from .models import DeeplLanguage
from .models import Lection
from .models import Question
from .models import Quiz
from .models import TranslatedQuestion
from .text import get_correct_message
from .text import get_incorrect_message
from .translate import get_translated_question_text


@cache_page(3600 * 24 * 1)
def quiz_list(request):
    quiz_list = Quiz.objects.all()
    context = {"quiz_list": quiz_list}
    return render(request, "quiz/quiz_list.html", context)


@cache_page(3600 * 24 * 1)
def search_quizzes(request):
    search_term = request.GET.get("q")
    level_one = request.GET.get("level_one")
    level_two = request.GET.get("level_two")
    level_three = request.GET.get("level_three")
    quiz_list = Quiz.objects.filter(
        name__icontains=search_term, level__in=[level_one, level_two, level_three]
    )
    context = {"quiz_list": quiz_list}
    return render(request, "quiz/partials/quiz_list.html", context)


@cache_page(3600 * 24 * 7)
def quiz_detail(request, slug, level):
    quiz = get_object_or_404(Quiz, slug=slug, level=level)
    lections = quiz.lection_set.all()
    context = {"quiz": quiz, "lections": lections}
    return render(request, "quiz/quiz_detail.html", context)


@cache_page(3600 * 24 * 7)
def question_detail(request, slug_quiz, level_quiz, slug_lection, id_question):
    quiz = get_object_or_404(Quiz, slug=slug_quiz, level=level_quiz)
    lection = get_object_or_404(Lection, slug=slug_lection, quiz=quiz)
    question = get_object_or_404(Question, id=id_question, lection=lection)
    context = {
        "question": question,
        "progress_percentage": question.progress_percentage(),
        "language_objects": DeeplLanguage.objects.all(),
    }
    return render(request, "quiz/question_detail.html", context)


def translate_question_text(request, id_question, id_language):
    language = get_object_or_404(DeeplLanguage, id=id_language)
    question = get_object_or_404(Question, id=id_question)
    question_translated_text = get_translated_question_text(question, language)
    context = {"translated_text": question_translated_text}
    return render(request, "quiz/partials/question_translated_text.html", context)


@csrf_exempt
@cache_page(3600 * 24 * 7)
def check_answer(request, id_question):
    question = get_object_or_404(Question, id=id_question)

    if question.type == 1:  # one text input
        answer_input_one = request.POST.get("answer_input_one")
        answers = question.answer_set.all()
        answer_one_is_correct = (
            answers[0].name.strip().lower() == answer_input_one.strip().lower()
        )
        question_answered_correctly = answer_one_is_correct
        context = {
            "question": question,
            "answer_one_is_correct": answer_one_is_correct,
            "correct_answer_one": answers[0].name.strip(),
        }

    elif question.type == 2:  # two text input
        answer_input_one = request.POST.get("answer_input_one")
        answer_input_two = request.POST.get("answer_input_two")
        answers = question.answer_set.all()
        answer_one_is_correct = (
            answers[0].name.strip().lower() == answer_input_one.strip().lower()
        )
        answer_two_is_correct = (
            answers[1].name.strip().lower() == answer_input_two.strip().lower()
        )
        question_answered_correctly = answer_one_is_correct and answer_two_is_correct
        context = {
            "question": question,
            "answer_one_is_correct": answer_one_is_correct,
            "answer_two_is_correct": answer_two_is_correct,
            "correct_answer_one": answers[0].name.strip(),
            "correct_answer_two": answers[1].name.strip(),
        }

    elif question.type == 5:  # one choice selection
        selected_answer_id = request.POST.get("selected_answer_id")
        selected_answer = get_object_or_404(Answer, id=selected_answer_id)
        question_answered_correctly = selected_answer.correct
        context = {"question": question, "selected_answer": selected_answer}

    if question_answered_correctly is True:
        context["correct_message"] = get_correct_message()
        response = render(request, "quiz/partials/question_correct.html", context)

    else:
        context["incorrect_message"] = get_incorrect_message()
        response = render(request, "quiz/partials/question_incorrect.html", context)

    trigger_client_event(
        response,
        "answerCheckedEvent",
        {},
    )
    return response


@cache_page(3600 * 24 * 7)
def update_progress_bar(request, id_question):
    question = get_object_or_404(Question, id=id_question)
    context = {"progress_percentage": question.progress_percentage(extra=1)}
    return render(request, "quiz/partials/progress_bar.html", context)
