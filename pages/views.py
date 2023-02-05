from __future__ import annotations

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from pages.forms import ContactForm
from pages.models import FlexPage
from quiz.models import Quiz
from affiliates.models import Book


def home_view(request):
    quiz_list = Quiz.objects.all()
    featured_books = Book.objects.filter(featured=True)
    context = {
        "quiz_list": quiz_list,
        "featured_books": featured_books,
        }
    return render(request, "pages/home.html", context)


def flexpage_detail_view(request, slug):
    object = get_object_or_404(FlexPage, slug=slug)
    context = {"page": object}
    return render(request, "pages/flexpage_detail.html", context)


def contact_view(request):
    if request.POST:
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "pages/contact_thanks.html")
    else:
        form = ContactForm()

    context = {"form": form}
    return render(request, "pages/contact.html", context)
