from django.contrib import admin

from affiliates.models import Book
from affiliates.models import BookAffiliateLink
from affiliates.models import CountryVisitor


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

@admin.register(CountryVisitor)
class CountryVisitorAdmin(admin.ModelAdmin):
    
    list_display = [
        "country_code",
        "views",
    ]