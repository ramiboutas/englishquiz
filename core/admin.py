from __future__ import annotations

from django.contrib import admin
from django.contrib import messages
from newsfeed.admin import NewsletterAdmin
from newsfeed.models import Newsletter

from core.models import Contact
from core.models import FlexPage

admin.site.unregister(Newsletter)


@admin.register(FlexPage)
class FlexPageAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "email",
        "message",
    ]

    readonly_fields = [
        "name",
        "email",
        "message",
        "responded",
        "responded_on",
        "responded_by",
        "subscribe",
        "subscribed",
        "created_on",
    ]

    list_filter = [
        "subscribe",
        "created_on",
        "responded",
        "responded_by",
    ]

    list_display = [
        "name",
        "email",
        "message",
        "responded",
    ]

    def save_model(self, request, obj, form, change):
        if obj.pk:
            obj.responded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Newsletter)
class NewsletterAdmin(NewsletterAdmin):
    def send_newsletters(self, request, queryset):
        newsletter_ids = list(queryset.values_list("id", flat=True))

        messages.add_message(
            request,
            messages.SUCCESS,
            "Sending selected newsletters(s) to the subscribers",
        )
