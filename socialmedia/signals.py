from __future__ import annotations

from django.db.models.signals import pre_save
from django.dispatch import receiver

from socialmedia.apis.linkedin import LinkedinPostAPI
from socialmedia.apis.telegram import TelegramAPI
from socialmedia.models import LinkedinPost
from socialmedia.models import TelegramMessage


@receiver(pre_save, sender=TelegramMessage)
def delete_telegram_message(sender, instance, **kwargs):
    """
    It deletes a message from Telegram
    """

    if instance.api_delete and not instance.api_deleted:
        try:
            TelegramAPI().delete_message(instance)
            instance.api_deleted = True
        except Exception as e:
            raise e


@receiver(pre_save, sender=LinkedinPost)
def delete_linkedin_company_post(sender, instance, **kwargs):
    """
    It deletes a post from the Linkedin company page
    """

    if instance.api_delete and not instance.api_deleted:
        try:
            LinkedinPostAPI().delete_post(instance.urn_li_share)
            instance.api_deleted = True
        except Exception as e:
            raise e
