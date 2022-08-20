
# newsfeed 
# https://github.com/saadmk11/test-django-newsfeed

from newsfeed.models import Newsletter
from celery import shared_task
from newsfeed.utils.send_newsletters import send_email_newsletter



@shared_task(bind=True)
def send_email_newsletter_task(newsletters_ids=None, respect_schedule=True):
    newsletters = None

    if newsletters_ids:
        newsletters = Newsletter.objects.filter(
            id__in=newsletters_ids
        )
    send_email_newsletter(
        newsletters=newsletters,
        respect_schedule=respect_schedule
    )