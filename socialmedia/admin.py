from __future__ import annotations

from django.contrib import admin

from .models import SocialPost


@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    search_fields = ["text"]
    readonly_fields = ["created_at", "updated_at", "promoted", "created_by"]
    list_filter = ["created_at", "updated_at", "promoted", "created_by"]
    list_display = ["text", "created_at", "promoted", "created_by"]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
