from django.contrib import admin

from affiliates.models import Book
from affiliates.models import BookAffiliateLink


class BookAffiliateLinkInline(admin.StackedInline):
    model = BookAffiliateLink
    extra = 5


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["category", "test_type", "level"]
    list_display = [
        "name",
        "category",
        "test_type",
        "level",
        "views",
    ]
    readonly_fields = ["views"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        BookAffiliateLinkInline,
    ]
