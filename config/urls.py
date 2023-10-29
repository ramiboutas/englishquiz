from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include
from django.urls import path
from django.views.generic.base import TemplateView

from core.views import favicon
from quiz.models import Quiz

info_dict = {
    "queryset": Quiz.objects.all(),
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": {
                "quiz": GenericSitemap(
                    info_dict,
                    priority=0.9,
                )
            }
        },
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("favicon.ico", favicon, name="favicon"),
    # third-party apps
    path("captcha/", include("captcha.urls")),
    path("markdownx/", include("markdownx.urls")),
    path("newsfeed/", include("newsfeed.urls", namespace="newsfeed")),
    # own apps
    path("blog/", include("blog.urls")),
    path("quiz/", include("quiz.urls")),
    path("", include("affiliates.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
