from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + (
        "blog_post_seconds",
        "number_of_social_posts",
    )
    readonly_fields = BaseUserAdmin.readonly_fields + (
        "blog_post_seconds",
        "number_of_social_posts",
    )
    fieldsets = (
        (None, {"fields": ("blog_post_seconds", "number_of_social_posts")}),
    ) + BaseUserAdmin.fieldsets
