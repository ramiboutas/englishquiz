from django.urls import path, include
from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap


urlpatterns = []

urlpatterns.extend([
        path(
            route='admin/',
            view=include(wagtailadmin_urls)
        ),
        path(
            route='',
            view=include(wagtail_urls)
        ),
        path(
            route='documents/',
            view=include(wagtaildocs_urls)
        ),
        path(
            route='sitemap.xml',
            view=sitemap
        )
    ])