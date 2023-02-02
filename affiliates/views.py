from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Q


from affiliates.models import Book, BookAffiliateLink

def _get_country_code(request):
    
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")    
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    
    g = GeoIP2()

    try:
        location = g.country(ip)
        return location["country_code"]
    except:
        return None
    


@cache_page(3600 * 24 * 1)
def book_list(request):
    book_list = Book.objects.all()
    context = {"book_list": book_list}
    return render(request, "affiliates/book_list.html", context)



def book_detail(request, slug):
    book = Book.objects.get(slug=slug)
    country_code = _get_country_code(request)
    country_code = "DE"
    affiliate_links = book.affiliate_links.filter(
        Q(country_code=country_code) | Q(is_global=True))
    context = {
        "book": book, 
        "affiliate_links": affiliate_links,
        "related_books": Book.objects.all() #book.get_related_books()
        }
    return render(request, "affiliates/book_detail.html", context)


@cache_page(3600 * 24 * 7)
def search_books(request):
    search_term = request.GET.get("q")
    level_one = request.GET.get("level_one")
    level_two = request.GET.get("level_two")
    level_three = request.GET.get("level_three")
    book_list = Book.objects.filter(
        name__icontains=search_term, 
        level__in=[level_one, level_two, level_three]
    )
    context = {"book_list": book_list}
    return render(request, "affiliates/partials/book_list.html", context)