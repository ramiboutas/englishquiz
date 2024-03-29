from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from affiliates.models import Book
from affiliates.models import BOOK_CATEGORIES
from affiliates.models import BOOK_LEVELS
from affiliates.models import BOOK_TEST_TYPES


@cache_page(3600 * 24 * 7)
def book_list(request):
    book_list = Book.objects.all()
    context = {
        "book_list": book_list,
        "book_levels": BOOK_LEVELS,
        "book_categories": BOOK_CATEGORIES,
        "book_test_types": BOOK_TEST_TYPES,
    }
    return render(request, "affiliates/book_list.html", context)


@cache_page(3600 * 24 * 7)
def book_detail(request, slug):
    book = Book.objects.get(slug=slug)
    context = {
        "book": book,
        "related_books": book.get_related_books(),
    }
    return render(request, "affiliates/book_detail.html", context)


@cache_page(3600 * 24 * 7)
def search_books(request):
    search_term = request.GET.get("q")
    test_types = request.GET.getlist("test_type")
    categories = request.GET.getlist("category")
    levels = request.GET.getlist("level")
    book_list = Book.objects.filter(
        name__icontains=search_term,
        test_type__in=test_types,
        category__in=categories,
        level__in=levels,
    )
    context = {"book_list": book_list}
    return render(request, "affiliates/partials/book_list.html", context)
