from __future__ import annotations

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from socialmedia.apis.facebook import FacebookPageAPI
from socialmedia.apis.instagram import InstagramAPI
from socialmedia.apis.linkedin import LinkedinCompanyPageAPI
from socialmedia.apis.telegram import TelegramAPI
from socialmedia.apis.twitter import TweetAPI
from socialmedia.models import (
    FacebookPost,
    InstagramPost,
    LinkedinPost,
    RegularSocialPost,
    ScheduledSocialPost,
    TelegramMessage,
    Tweet,
)
from socialmedia.tasks import (
    create_image_from_regular_social_post_instance,
    create_image_from_scheduled_social_post_instance,
    promote_scheduled_social_post_instance,
)


@receiver(post_save, sender=ScheduledSocialPost)
def schedule_social_post_for_promoting(sender, instance, **kwargs):
    """
    Schedules a social post (Social Post = Post in Linkedin, Message in Telegram, Tweet in Twitter)
    """

    promote_scheduled_social_post_instance.apply_async(
        eta=instance.promote_date, kwargs={"pk": instance.pk}
    )


@receiver(post_save, sender=RegularSocialPost)
def trigger_image_creation_task_for_regular_posts(sender, instance, **kwargs):
    """
    Triggers the creation of images - RegularSocialPost
    """
    instance.refresh_from_db()

    if instance.image_text and not instance.image:
        create_image_from_regular_social_post_instance.apply_async(
            countdown=1, kwargs={"pk": instance.pk}
        )


@receiver(post_save, sender=ScheduledSocialPost)
def trigger_image_creation_task_for_scheduled_posts(sender, instance, **kwargs):
    """
    Triggers the creation of images - ScheduledSocialPost
    """
    instance.refresh_from_db()

    if instance.image_text and not instance.image:
        create_image_from_scheduled_social_post_instance.apply_async(
            countdown=1, kwargs={"pk": instance.pk}
        )


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
def delete_tweet(sender, instance, **kwargs):
    """
    It deletes a tweet
    """

    if instance.api_delete and not instance.api_deleted:
        try:
            TweetAPI().delete(instance)
            instance.api_deleted = True
        except Exception as e:
            raise e


@receiver(pre_save, sender=LinkedinPost)
def delete_linkedin_company_ugc_post(sender, instance, **kwargs):
    """
    It deletes a UGC post from the Linkedin company page
    """

    if instance.api_delete and not instance.api_deleted:
        try:
            LinkedinCompanyPageAPI().delete_ugcPost(instance)
            instance.api_deleted = True
        except Exception as e:
            raise e


@receiver(pre_save, sender=FacebookPost)
def delete_facebook_post(sender, instance, **kwargs):
    """
    It deletes a post from the Facebook company page
    """

    if instance.api_delete and not instance.api_deleted:
        try:
            FacebookPageAPI().delete_post(instance)
            instance.api_deleted = True
        except Exception as e:
            raise e


@receiver(pre_save, sender=InstagramPost)
def delete_instagram_post(sender, instance, **kwargs):
    """
    It deletes a post from the Instagram business account
    """

    if instance.api_delete and not instance.api_deleted:
        try:
            InstagramAPI().delete_post(instance)
            instance.api_deleted = True
        except Exception as e:
            raise e
