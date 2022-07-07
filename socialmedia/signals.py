from time import sleep
from django.dispatch import receiver
from django.db.models.signals import post_save

from wagtail.signals import page_published
from puput.models import EntryPage

from . import tasks as socialmedia_tasks
from .models import ScheduledSocialPost


@receiver(page_published, sender=EntryPage)
def schedule_blog_entry_for_promoting(sender, instance, *args, **kwargs):
    """
    Calls to task functions for promoting in social media a blog entry instance
    """
     
    promote_in_telegram = True
    promote_in_linkedin = True
    promote_in_twitter = True

    # REFACTOR THIS FUNCTIONS INTO ONE -> promote_blog_post_instance(instance)

    if promote_in_telegram:
        socialmedia_tasks.promote_post_instance_in_telegram.apply_async(instance, countdown=5)

    if promote_in_linkedin:
        socialmedia_tasks.promote_post_instance_in_linkedin.apply_async(instance, countdown=5)

    if promote_in_twitter:
        socialmedia_tasks.promote_post_instance_in_twitter.apply_async(instance, countdown=5)



@receiver(post_save, sender=ScheduledSocialPost)
def schedule_social_post_for_promoting(sender, instance, **kwargs):
    """
    Schedules a social post (Social Post = Post in Linkedin, Message in Telegram, Tweet in Twitter)
    """

    if instance.promote:
        socialmedia_tasks.promote_scheduled_social_post_instance.apply_async(eta=instance.promote_date, countdown=10, kwargs={"pk":instance.pk})
