from django.contrib import admin

from .models import ScheduledSocialPost, RegularSocialPost


admin.site.register(ScheduledSocialPost)
admin.site.register(RegularSocialPost)
