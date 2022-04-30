import random
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page, never_cache


from django_htmx.http import trigger_client_event

from .models import Quiz, Lection, Question, Answer


@cache_page(3600 * 6)
def home(request):
    quiz_list = Quiz.objects.all()
    context ={'quiz_list': quiz_list}
    return render(request, 'home.html', context)

@never_cache
def search_quizzes(request):
    search_term = request.GET.get('search_term')
    quiz_list = Quiz.objects.filter(name__icontains=search_term)
    context = {'quiz_list': quiz_list}
    return render(request, 'partials/quiz_list.html', context)


@cache_page(3600 * 6)
def quiz_detail(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    lections = quiz.lection_set.all()
    context ={'quiz':quiz, 'lections': lections}
    return render(request, 'quiz_detail.html', context)


@cache_page(3600 * 6)
def question_detail(request, slug_quiz, slug_lection, id_question):
    quiz = get_object_or_404(Quiz, slug=slug_quiz)
    lection = get_object_or_404(Lection, slug=slug_lection, quiz=quiz)
    question = get_object_or_404(Question, id=id_question, lection=lection)
    questions = list(Question.objects.filter(lection=lection))
    index = questions.index(question)
    number_of_questions = questions.__len__()
    progress_percentage = int(index*100/number_of_questions)
    context ={'question': question, 'progress_percentage': progress_percentage}
    return render(request, 'question_detail.html', context)

@csrf_exempt
@never_cache
def check_answer(request, slug_quiz, slug_lection, id_question):
    question = get_object_or_404(Question, id=id_question)

    if question.type == 1: # one text input
        answer_input_one = request.POST.get('answer_input_one')
        answers = question.answer_set.all()
        answer_one_is_correct = answers[0].name.strip().lower()==answer_input_one.strip().lower()
        question_answered_correcty = answer_one_is_correct
        context = {
            'question': question,
            'answer_one_is_correct': answer_one_is_correct,
            'correct_answer_one': answers[0].name.strip(),
        }

    elif question.type == 2: # two text input
        answer_input_one = request.POST.get('answer_input_one')
        answer_input_two = request.POST.get('answer_input_two')
        answers = question.answer_set.all()
        answer_one_is_correct = answers[0].name.strip().lower()==answer_input_one.strip().lower()
        answer_two_is_correct = answers[1].name.strip().lower()==answer_input_two.strip().lower()
        question_answered_correcty = answer_one_is_correct and answer_two_is_correct
        context = {
            'question': question,
            'answer_one_is_correct': answer_one_is_correct,
            'answer_two_is_correct': answer_two_is_correct,
            'correct_answer_one': answers[0].name.strip(),
            'correct_answer_two': answers[1].name.strip(),
        }

    elif question.type == 5: # one choice selection
        selected_answer_id = request.POST.get('selected_answer_id')
        selected_answer = get_object_or_404(Answer, id=selected_answer_id)
        question_answered_correcty = selected_answer.correct
        context = {'question': question, 'selected_answer': selected_answer}

    if question_answered_correcty == True:
        correct_messages = ["Great!", "Correct!", "Well done!", "Terrific!", "Fantastic!", "Excelent!", "Super!", "Marvellous!", "Outstanding!",  ":)"]
        context['correct_message'] = random.choice(correct_messages)
        response = render(request, 'partials/question_correct.html', context)

    else:
        incorrect_messages = ["Next time you'll get it!", "There's a more accurate answer!", "Oops!", "Wrong :(", "Not quite correct!", ":("]
        context['incorrect_message'] = random.choice(incorrect_messages)
        response = render(request, 'partials/question_incorrect.html',  context)

    trigger_client_event(response, "answerCheckedEvent", { },) # this is the trigger event
    return response


@cache_page(3600 * 6)
def update_progress_bar(request, slug_quiz, slug_lection, id_question):
    quiz = get_object_or_404(Quiz, slug=slug_quiz)
    lection = get_object_or_404(Lection, slug=slug_lection, quiz=quiz)
    question = get_object_or_404(Question, id=id_question, lection=lection)
    questions = list(Question.objects.filter(lection=lection))
    index = questions.index(question) + 1
    number_of_questions = questions.__len__()
    progress_percentage = int(index*100/number_of_questions)
    context ={'progress_percentage': progress_percentage}
    return render(request, 'partials/progress_bar.html', context)
