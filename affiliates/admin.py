from django.contrib import admin
from nested_inline.admin import NestedModelAdmin
from nested_inline.admin import NestedStackedInline


from affiliates.models import Book, BookAffiliateLink


class BookAffiliateLinkInline(admin.StackedInline):
    model = BookAffiliateLink
    extra = 5
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["name"]
    prepopulated_fields = {"slug": ("name",)}

    inlines = [
        BookAffiliateLinkInline,
    ]
