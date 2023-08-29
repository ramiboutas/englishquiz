from __future__ import annotations

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from newsfeed.models import Newsletter
from newsfeed.models import Subscriber
from newsfeed.utils.send_newsletters import send_email_newsletter

from core.models import Contact


@shared_task(bind=True)
def send_email_newsletter(newsletters_ids=None, respect_schedule=True):
    newsletters = None

    if newsletters_ids:
        newsletters = Newsletter.objects.filter(id__in=newsletters_ids)
    send_email_newsletter(newsletters=newsletters, respect_schedule=respect_schedule)


@shared_task(bind=True)
def send_email_to_contacted_person(self, **kwargs):
    contact = Contact.objects.get(pk=kwargs["pk"])
    send_mail(
        f"Contact #{contact.pk} | English Stuff Online",
        contact.response,
        settings.EMAIL_HOST_USER,
        [contact.email],
        fail_silently=False,
    )
    contact.responded = True
    contact.responded_on = timezone.now()
    contact.save()


@shared_task(bind=True)
def subscribe_contacted_person_to_newsletter(self, **kwargs):
    instance = Contact.objects.get(pk=kwargs["pk"])
    subscriber, created = Subscriber.objects.get_or_create(email_address=instance.email)
    if created or not subscriber.subscribed:
        subscriber.send_verification_email(created)
    instance.subscribed = True
    instance.save()
