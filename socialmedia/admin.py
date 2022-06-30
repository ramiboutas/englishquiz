from django.contrib import admin

from .models import ScheduledSocialPost, RegularSocialPost, ScheduledLargeSocialPost, LargeSocialPost


admin.site.register(ScheduledSocialPost)
admin.site.register(RegularSocialPost)

admin.site.register(ScheduledLargeSocialPost)
admin.site.register(LargeSocialPost)
