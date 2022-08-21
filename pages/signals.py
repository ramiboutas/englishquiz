from django.dispatch import receiver
from django.db.models.signals import post_save

from pages.tasks import send_email_to_contacted_person, subscribe_contacted_person_to_newsletter

from .models import Contact
from django.conf import settings





@receiver(post_save, sender=Contact)
def manage_contact_instance(sender, instance, **kwargs):
    """
    It sends an email to the  person who contacted us
    
    """
    
    instance.refresh_from_db()

    if instance.response and not instance.responded:
        send_email_to_contacted_person.apply_async(countdown=5, kwargs={"pk":instance.pk})
        
    if instance.subscribe and not instance.subscribed:
        subscribe_contacted_person_to_newsletter.apply_async(countdown=2, kwargs={"pk":instance.pk})


