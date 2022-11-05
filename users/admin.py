from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "blog_post_seconds",
        "social_posts",
        "quiz_questions",
        "total_euros",
    )
    readonly_fields = BaseUserAdmin.readonly_fields + (
        "blog_post_seconds",
        "social_posts",
        "quiz_questions",
        "total_euros",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "blog_post_seconds",
                    "social_posts",
                    "quiz_questions",
                    "total_euros",
                )
            },
        ),
    ) + BaseUserAdmin.fieldsets
