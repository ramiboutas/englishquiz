
from django.contrib import admin

from core.models import CountryVisitor


@admin.register(CountryVisitor)
class CountryVisitorAdmin(admin.ModelAdmin):

    list_display = [
        "country_code",
        "views",
    ]
