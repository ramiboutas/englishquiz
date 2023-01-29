from django.contrib import admin

# Register your models here.


from affiliates.models import Book



@affiliates.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["views"]
    list_filter = ["name"]
    prepopulated_fields = {"slug": ("name",)}