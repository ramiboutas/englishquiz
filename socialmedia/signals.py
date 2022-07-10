from shutil import ExecError
from time import sleep
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from wagtail.signals import page_published
from puput.models import EntryPage

from .api_twitter import TweetAPI
from .api_telegram import TelegramAPI
from . import tasks as socialmedia_tasks
from .models import ScheduledSocialPost, TelegramMessage, Tweet


@receiver(page_published, sender=EntryPage)
def schedule_blog_entry_for_promoting(sender, instance, *args, **kwargs):
    """
    Calls to task function for promoting in social media a blog entry instance
    """
    socialmedia_tasks.promote_blog_post_instance.apply_async(countdown=10, kwargs={"pk":instance.pk})



@receiver(post_save, sender=ScheduledSocialPost)
def schedule_social_post_for_promoting(sender, instance, **kwargs):
    """
    Schedules a social post (Social Post = Post in Linkedin, Message in Telegram, Tweet in Twitter)
    """

    if instance.promote:
        socialmedia_tasks.promote_scheduled_social_post_instance.apply_async(eta=instance.promote_date, countdown=10, kwargs={"pk":instance.pk})


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



@receiver(pre_save, sender=Tweet)
def delete_telegram_message(sender, instance, **kwargs):
    """
    It deletes a message from Twitter
    """

    if instance.api_delete and not instance.api_deleted:
        try:
            TweetAPI().delete(instance)
            instance.api_deleted = True
        except Exception as e:
            raise e