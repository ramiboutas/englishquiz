from django.contrib import admin, messages

from newsfeed.admin import NewsletterAdmin
from newsfeed.models import Newsletter

from .tasks import send_email_newsletter_task
from .models import Contact, FlexPage

admin.site.unregister(Newsletter)

class FlexPageAdmin(admin.ModelAdmin):
    pass



class ContactAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'message', 'responded', 'responded_on', 'responded_by', 'subscribe', 'subscribed', 'created_on']
    list_filter = ['subscribe', 'created_on', 'responded', 'responded_by']
    list_display = ['name', 'email', 'message', 'responded']


    def save_model(self, request, obj, form, change):
        if obj.pk:
            obj.responded_by = request.user
        super().save_model(request, obj, form, change)


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