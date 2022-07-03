from django.contrib import admin

from .models import ScheduledSocialPost, RegularSocialPost



class ScheduledSocialPostAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['created', 'updated']
    list_filter = ['promote', 'created', 'updated']

class RegularSocialPostAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['created', 'updated', 'promoted']
    list_filter = ['promote', 'created', 'updated', 'promoted']



admin.site.register(ScheduledSocialPost, ScheduledSocialPostAdmin)
admin.site.register(RegularSocialPost, RegularSocialPostAdmin)
