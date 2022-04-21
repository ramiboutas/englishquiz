from django.shortcuts import render, get_object_or_404

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
