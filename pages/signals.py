from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Contact



@receiver(post_save, sender=Contact)
def send_contact_response_email(sender, instance, **kwargs):
    """
    TO DO /// It sends an email to the  person who contacted
    """
    
    if instance.response:
        pass


