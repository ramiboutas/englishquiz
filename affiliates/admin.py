from django.contrib import admin

from affiliates.models import Book


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
