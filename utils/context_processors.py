from django.conf import settings
from django.utils import timezone


def get_copyright_year(year):
    if year > 2022:
        return f'2022 - {year}'
    return '2022'


def general(request):

    return {
        'copyright_year': get_copyright_year(timezone.now().year),
        'site_title': settings.SITE_TITLE,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
    }
