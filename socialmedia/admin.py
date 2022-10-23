from __future__ import annotations

from django.contrib import admin

from .models import (
    BackgroundImage,
    FacebookPost,
    InstagramPost,
    LinkedinPost,
    RegularSocialPost,
    ScheduledSocialPost,
    TelegramMessage,
    Tweet,
)


@admin.register(BackgroundImage)
class BackgroundImageAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "image",
    ]


@admin.register(ScheduledSocialPost)
class ScheduledSocialPostAdmin(admin.ModelAdmin):
    search_fields = [
        "text",
    ]

    readonly_fields = [
        "created",
        "updated",
        "created_by",
    ]

    list_filter = [
        "created",
        "updated",
        "promote_date",
        "created_by",
    ]

    list_display = [
        "text",
        "created",
        "promote_date",
        "created_by",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(RegularSocialPost)
class RegularSocialPostAdmin(admin.ModelAdmin):
    search_fields = [
        "text",
    ]

    readonly_fields = [
        "created",
        "updated",
        "promoted",
        "created_by",
    ]

    list_filter = [
        "created",
        "updated",
        "promoted",
        "created_by",
    ]

    list_display = [
        "text",
        "created",
        "promoted",
        "created_by",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    search_fields = [
        "text",
    ]

    readonly_fields = [
        "text",
        "created_at",
        "favorite_count",
        "twitter_id",
        "id_str",
        "retweet_count",
        "twitter_url",
        "api_deleted",
    ]

    list_filter = [
        "created_at",
    ]

    list_display = [
        "text",
        "twitter_id",
        "retweet_count",
        "favorite_count",
    ]


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


@admin.register(FacebookPost)
class FacebookPostAdmin(admin.ModelAdmin):
    search_fields = [
        "text",
    ]

    readonly_fields = [
        "facebook_id",
        "text",
        "date",
        "api_deleted",
    ]

    list_filter = [
        "date",
    ]

    list_display = [
        "text",
        "facebook_id",
        "api_deleted",
    ]


@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    search_fields = [
        "text",
    ]

    readonly_fields = [
        "instagram_id",
        "text",
        "date",
        "api_deleted",
    ]

    list_filter = [
        "date",
    ]

    list_display = [
        "text",
        "instagram_id",
        "api_deleted",
    ]
