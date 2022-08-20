from django.contrib import admin, messages

from newsfeed.admin import NewsletterAdmin
from newsfeed.models import Newsletter

from .tasks import send_email_newsletter_task
from .models import Contact, FlexPage

admin.site.unregister(Newsletter)

class FlexPageAdmin(admin.ModelAdmin):
    pass



class ContactAdmin(admin.ModelAdmin):
    pass




class NewsletterAdmin(NewsletterAdmin):

    def send_newsletters(self, request, queryset):
        newsletter_ids = list(queryset.values_list('id', flat=True))

        send_email_newsletter_task.delay(
            newsletters_ids=newsletter_ids,
            respect_schedule=False
        )
        messages.add_message(
            request,
            messages.SUCCESS,
            'Sending selected newsletters(s) to the subscribers',
        )






admin.site.register(FlexPage, FlexPageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Newsletter, NewsletterAdmin)