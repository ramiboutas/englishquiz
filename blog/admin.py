from __future__ import annotations

from django.contrib import admin

from .models import BlogPost
from markdownx.admin import MarkdownxModelAdmin


@admin.register(BlogPost)
class BlogPostAdmin(MarkdownxModelAdmin):

    search_fields = ["title", "content"]
    readonly_fields = [
        "created",
        "updated",
        "created_by",
        "views",
        "promoted",
        "reading_time",
        "reading_time_in_seconds",
    ]
    prepopulated_fields = {
        "slug": ("title",),
    }

    list_filter = ["level", "public", "created_by", "created"]
    list_display = [
        "title",
        "level",
        "public",
        "created_by",
        "views",
        "created",
        "reading_time",
        "reading_time_in_seconds",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
