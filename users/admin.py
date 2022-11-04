from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ("whatever",)  # list_display is a tuple
    fieldsets = ((None, {"fields": ("whatever",)}),) + BaseUserAdmin.fieldsets
