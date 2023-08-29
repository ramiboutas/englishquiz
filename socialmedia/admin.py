from __future__ import annotations

from django.contrib import admin

from .models import LinkedinPost
from .models import SocialPost
from .models import TelegramMessage


@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    search_fields = [
        "text",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
        "promoted",
        "created_by",
    ]

    list_filter = [
        "created_at",
        "updated_at",
        "promoted",
        "created_by",
    ]

    list_display = [
        "text",
        "created_at",
        "promoted",
        "created_by",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TelegramMessage)
class TelegramMessageAdmin(admin.ModelAdmin):
    search_fields = [
        "text",
    ]

    readonly_fields = [
        "text",
        "message_id",
        "chat_id",
        "link",
        "date",
        "api_deleted",
    ]

    list_filter = [
        "date",
        "api_deleted",
    ]

    list_display = [
        "text",
        "message_id",
        "link",
        "date",
        "api_deleted",
    ]


@admin.register(LinkedinPost)
class LinkedinPostAdmin(admin.ModelAdmin):
    search_fields = [
        "text",
    ]

    readonly_fields = [
        "urn_li_share",
        "text",
        "media_asset",
        "click_count",
        "comment_count",
        "engagement",
        "impression_count",
        "like_count",
        "share_count",
        "api_deleted",
    ]

    list_filter = [
        "date",
        "api_deleted",
    ]

    list_display = [
        "text",
        "urn_li_share",
        "api_deleted",
    ]
