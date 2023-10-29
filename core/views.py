from __future__ import annotations

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.http import require_GET
from django.views import View

from affiliates.models import Book
from core.forms import ContactForm
from core.models import FlexPage
from quiz.models import Quiz


@cache_page(3600 * 24 * 7)
def home_view(request):
    quiz_list = Quiz.objects.all()
    featured_books = Book.objects.filter(featured=True)
    context = {
        "quiz_list": quiz_list,
        "featured_books": featured_books,
    }
    return render(request, "core/home.html", context)


@cache_page(3600 * 24 * 30)
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


class AdsView(View):
    """Replace pub-0000000000000000 with your own publisher ID"""

    line = "google.com, pub-3031639002739313, DIRECT, f08c47fec0942fa0"

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.line)
