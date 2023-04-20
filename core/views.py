from __future__ import annotations

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.http import HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from affiliates.models import Book
from core.forms import ContactForm
from core.models import FlexPage
from quiz.models import Quiz


def home_view(request):
    quiz_list = Quiz.objects.all()
    featured_books = Book.objects.filter(featured=True)
    context = {
        "quiz_list": quiz_list,
        "featured_books": featured_books,
    }
    return render(request, "core/home.html", context)


def flexpage_detail_view(request, slug):
    object = get_object_or_404(FlexPage, slug=slug)
    context = {"page": object}
    return render(request, "core/flexpage_detail.html", context)


def contact_view(request):
    if request.POST:
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "core/contact_thanks.html")
    else:
        form = ContactForm()

    context = {"form": form}
    return render(request, "core/contact.html", context)


@require_GET
@cache_control(max_age=60 * 60 * 24 * 30, immutable=True, public=True)
def favicon(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            + '<text y=".9em" font-size="90">🇬🇧</text>'
            + "</svg>"
        ),
        content_type="image/svg+xml",
    )
