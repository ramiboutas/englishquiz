from __future__ import annotations

import auto_prefetch
from django.conf import settings
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


class SocialPost(auto_prefetch.Model):
    """
    Social Post what will be promoted in social media on a daily basis.

    """

    text = models.TextField(max_length=2000)
    file = models.ImageField(upload_to="socialposts/files/", null=True, blank=True)
    promote_in_linkedin = models.BooleanField(default=True)
    promote_in_twitter = models.BooleanField(default=True)
    promote_in_telegram = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)
    promoted = models.BooleanField(default=False, editable=False)

    created_by = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

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
    api_delete = models.BooleanField(verbose_name="Delete from Telegram", default=False)
    api_deleted = models.BooleanField(
        verbose_name="Deleted from Telegram", default=False
    )

    def __str__(self) -> str:
        return self.text[:100]
