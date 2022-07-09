from django.contrib import admin

from .models import ScheduledSocialPost, RegularSocialPost, Tweet



class ScheduledSocialPostAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['created', 'updated']
    list_filter = ['promote', 'created', 'updated']

class RegularSocialPostAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['created', 'updated', 'promoted']
    list_filter = ['promote', 'created', 'updated', 'promoted']


class TweetAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['created_at', 'favorite_count', 'twitter_id', 'id_str', 'retweet_count', 'twitter_url']
    list_filter = ['created_at']
    list_display = ['text', 'twitter_id', 'retweet_count', 'favorite_count',]


admin.site.register(ScheduledSocialPost, ScheduledSocialPostAdmin)
admin.site.register(RegularSocialPost, RegularSocialPostAdmin)

admin.site.register(Tweet, TweetAdmin)

