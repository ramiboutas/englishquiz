from __future__ import annotations

import random
import auto_prefetch
from django.conf import settings
from django.db import models


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

    @classmethod
    def get_random_object_to_promote(cls):
        # Promote post without image for the moment
        posts = cls.objects.filter(promoted=False, file=None)
        if not posts.exists():
            qs = cls.objects.all()
            qs.update(promoted=False)
            return qs[0]
        return random.choice(list(posts))
