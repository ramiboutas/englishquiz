from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + (
        "blog_post_seconds",
        "number_of_social_posts",
        "number_of_quiz_questions",
    )
    readonly_fields = BaseUserAdmin.readonly_fields + (
        "blog_post_seconds",
        "number_of_social_posts",
        "number_of_quiz_questions",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "blog_post_seconds",
                    "number_of_social_posts",
                    "number_of_quiz_questions",
                )
            },
        ),
    ) + BaseUserAdmin.fieldsets
