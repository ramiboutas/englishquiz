from __future__ import annotations

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class BackgroundImage(models.Model):
    """ "
    Definition of a Background Image object - used to create images with text
    """

    name = models.CharField(
        max_length=20,
        null=True,
    )

    image = models.ImageField(
        upload_to="socialposts/backgrounds/",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class AbstractSocialPost(models.Model):
    """
    Common information about a Social Post (Abstract Model)
    Social Post = Post in Linkedin, Message in Telegram, Tweet in Twitter
    Limit of characters: Twitter: 280   Instagram: 2,200     Facebook: 63,206   Telegram: 4,400
    """

    text = models.TextField(max_length=2000)

    image_text = models.TextField(
        max_length=100,
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to="socialposts/images/",
        null=True,
        blank=True,
    )

    background_image_obj = models.ForeignKey(
        BackgroundImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    share_image = models.BooleanField(
        verbose_name="Share image",
        default=False,
    )

    promote_in_linkedin = models.BooleanField(
        verbose_name="Promote in Linkedin",
        default=True,
    )

    promote_in_twitter = models.BooleanField(
        verbose_name="Promote in Twitter",
        default=True,
    )

    promote_in_telegram = models.BooleanField(
        verbose_name="Promote in Telegram",
        default=True,
    )

    promote_in_facebook = models.BooleanField(
        verbose_name="Promote in Facebook",
        default=True,
    )

    promote_in_instagram = models.BooleanField(
        verbose_name="Promote in Instagram",
        default=False,
    )

    created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, editable=False
    )

    updated = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
        editable=False,
    )

    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class ScheduledSocialPost(AbstractSocialPost):
    """
    Social Post what will be promoted in social media on a specific data and time.
    """

    promote_date = models.DateTimeField()

    def __str__(self):
        return self.text


class RegularSocialPost(AbstractSocialPost):
    """
    Social Post what will be promoted in social media on a daily basis.
    """

    promoted = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.text


class LinkedinPost(models.Model):
    """ "
    Definition of a Linkedin Post object
    """

    urn_li_share = models.CharField(max_length=50)

    media_asset = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    text = models.TextField(max_length=1000)

    date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    click_count = models.PositiveIntegerField(null=True)

    comment_count = models.PositiveIntegerField(null=True)

    engagement = models.FloatField(null=True)

    impression_count = models.PositiveIntegerField(null=True)

    like_count = models.PositiveIntegerField(null=True)

    share_count = models.PositiveIntegerField(null=True)

    api_delete = models.BooleanField(
        verbose_name="Delete from Linkedin",
        default=False,
        help_text="It gets deleted from Linkedin after clicking on Save",
    )

    api_deleted = models.BooleanField(
        verbose_name="Already deleted from Linkedin", default=False
    )

    def __str__(self) -> str:
        return self.text[:100]


class TelegramMessage(models.Model):
    """ "
    Definition of a Telegram Message object
    """

    chat_id = models.BigIntegerField()

    message_id = models.BigIntegerField()

    link = models.CharField(max_length=100)

    text = models.TextField(max_length=4000)

    date = models.DateTimeField()

    api_delete = models.BooleanField(
        verbose_name="Delete from Telegram",
        default=False,
        help_text="It gets deleted from Telegram after clicking on Save",
    )

    api_deleted = models.BooleanField(
        verbose_name="Already deleted from Telegram", default=False
    )

    def __str__(self) -> str:
        return self.text[:100]


class Tweet(models.Model):
    """ "
    Definition of a Tweet Post object
    """

    twitter_id = models.PositiveBigIntegerField()

    id_str = models.CharField(max_length=30)

    text = models.TextField(max_length=300)

    twitter_url = models.URLField(null=True)

    created_at = models.DateTimeField()

    retweet_count = models.PositiveIntegerField()

    favorite_count = models.PositiveIntegerField()

    api_delete = models.BooleanField(
        verbose_name="Delete from Twitter",
        default=False,
        help_text="It gets deleted from Twitter after clicking on Save",
    )

    api_deleted = models.BooleanField(
        verbose_name="Already deleted from Twitter", default=False
    )

    def __str__(self) -> str:
        return self.text[:100]

    def save(self, *args, **kwargs):
        self.twitter_url = (
            f"https://twitter.com/{settings.TWITTER_USERNAME}/status/{self.id_str}"
        )
        super().save(*args, **kwargs)


class FacebookPost(models.Model):
    """ "
    Definition of a Facebook Post object
    """

    facebook_id = models.CharField(max_length=50)

    text = models.TextField(max_length=1000)

    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    api_delete = models.BooleanField(
        verbose_name="Delete from Facebook",
        default=False,
        help_text="It gets deleted from Facebook after clicking on Save",
    )

    api_deleted = models.BooleanField(
        verbose_name="Already deleted from Facebook", default=False
    )

    def __str__(self) -> str:
        return self.text[:100]


class InstagramPost(models.Model):
    """ "
    Definition of an Instagram Post object
    """

    instagram_id = models.CharField(max_length=50)

    text = models.TextField(max_length=1000)

    date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    api_delete = models.BooleanField(
        verbose_name="Delete from Instagram",
        default=False,
        help_text="It gets deleted from Instagram after clicking on Save",
    )

    api_deleted = models.BooleanField(
        verbose_name="Already deleted from Instagram",
        default=False,
    )

    def __str__(self) -> str:
        return self.text[:100]
