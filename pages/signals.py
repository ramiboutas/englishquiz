from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Contact
from django.conf import settings


from django.core.mail import send_mail



@receiver(post_save, sender=Contact)
def send_contact_response_email(sender, instance, **kwargs):
    """
    TO DO /// It sends an email to the  person who contacted
    """
    
    if instance.response:
        send_mail(
            'English Stuff Online | Contact request',
            instance.response,
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
        )


