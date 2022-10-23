"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic.base import TemplateView

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
    # third-party apps
    path("captcha/", include("captcha.urls")),
    path("markdownx/", include("markdownx.urls")),
    path("newsfeed/", include("newsfeed.urls", namespace="newsfeed")),
    # own apps
    path("social-media/", include("socialmedia.urls")),
    path("blog/", include("blog.urls")),
    path("quiz/", include("quiz.urls")),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
