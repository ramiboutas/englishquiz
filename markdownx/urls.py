"""
**MarkdownX** default URLs, to be added to URLs in the main project.

See URLs in :doc:`../../example` to learn more.
"""
from __future__ import annotations

from django.urls import re_path

from .views import ImageUploadView, MarkdownifyView

urlpatterns = [
    re_path("upload/", ImageUploadView.as_view(), name="markdownx_upload"),
    re_path("markdownify/", MarkdownifyView.as_view(), name="markdownx_markdownify"),
]
