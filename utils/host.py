from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError, GeoIP2Error

from core.models import CountryVisitor

def get_country_code(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    g = GeoIP2()

    try:
        location = g.country(ip)
        return location["country_code"]
    except KeyError:
        pass
    except AddressNotFoundError:
        pass
    finally:
        return None



def add_country_visitor(request):
    country_code = get_country_code(request)
    if country_code:
        country_visitor, _ = CountryVisitor.objects.get_or_create(country_code=country_code)
        country_visitor.add_view()
    return country_code
