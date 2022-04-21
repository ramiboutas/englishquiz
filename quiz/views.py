from django.shortcuts import render, get_object_or_404

from django_htmx.http import trigger_client_event

from .models import Quiz, Lection, Question, Answer


def quiz_list(request):
    quiz_list = Quiz.objects.all()
    context ={'quiz_list': quiz_list}
    return render(request, 'quiz_list.html', context)


def quiz_detail(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    lections = quiz.lection_set.all()
    context ={'quiz':quiz, 'lections': lections}
    return render(request, 'quiz_detail.html', context)


def question_detail(request, slug_quiz, slug_lection, id_question):
    quiz = get_object_or_404(Quiz, slug=slug_quiz)
    lection = get_object_or_404(Lection, slug=slug_lection, quiz=quiz)
    question = get_object_or_404(Question, id=id_question, lection=lection)
    context ={'question': question}
    return render(request, 'question_detail.html', context)



def check_answer(request, slug_quiz, slug_lection, id_question):
    question = get_object_or_404(Question, id=id_question)
    selected_answer_id = request.POST.get('selected_answer_id')
    selected_answer = get_object_or_404(Answer, id=selected_answer_id)
    context = {'question': question, 'selected_answer': selected_answer}
    if selected_answer.correct == True:
        response = render(request, 'partials/question_correct.html', context)
    else:
        response = render(request, 'partials/question_incorrect.html',  context)
    trigger_client_event(response, "answerCheckedEvent", { },) # this is the trigger event
    return response
