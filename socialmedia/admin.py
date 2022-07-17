from django.contrib import admin

from .models import (LinkedinPost, ScheduledSocialPost, 
                    RegularSocialPost, 
                    TelegramMessage,
                    Tweet,
                    LinkedinPost,
                    FacebookPost,
                    )



class ScheduledSocialPostAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['created', 'updated']
    list_filter = ['created', 'updated']

class RegularSocialPostAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['created', 'updated', 'promoted']
    list_filter = ['created', 'updated', 'promoted']


class TweetAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['text', 'created_at', 'favorite_count', 'twitter_id', 'id_str', 'retweet_count', 'twitter_url', 'api_deleted']
    list_filter = ['created_at']
    list_display = ['text', 'twitter_id', 'retweet_count', 'favorite_count',]


class TelegramMessageAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['text', 'message_id', 'chat_id', 'link', 'date', 'api_deleted']
    list_filter = ['date']
    # list_display = ['text', 'twitter_id', 'retweet_count', 'favorite_count',]


class LinkedinPostAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['urn_li_share', 'text', 'click_count', 'comment_count', 'engagement', 'impression_count', 'like_count', 'share_count', 'api_deleted']
    list_filter = ['date']


class FacebookPostAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ['facebook_id', 'text', 'date', 'api_deleted']
    list_filter = ['date']

admin.site.register(ScheduledSocialPost, ScheduledSocialPostAdmin)
admin.site.register(RegularSocialPost, RegularSocialPostAdmin)


admin.site.register(Tweet, TweetAdmin)
admin.site.register(TelegramMessage, TelegramMessageAdmin)
admin.site.register(LinkedinPost, LinkedinPostAdmin)
admin.site.register(FacebookPost, FacebookPostAdmin)


