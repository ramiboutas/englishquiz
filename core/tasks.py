from django.utils import timezone
from celery import shared_task
from newsfeed.models import Subscriber


@shared_task(bind=True)
def remove_unverified_newsletter_subscribers(self, **kwargs):
    qs = Subscriber.objects.filter(
        verification_sent_date__lt=timezone.now() - timezone.timedelta(days=4),
        verified = False,
        subscribed = False,
        )
    qs.delete()


