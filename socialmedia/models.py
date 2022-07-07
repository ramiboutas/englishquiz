from pyexpat import model
from django.db import models

# Create your models here.

SOCIAL_PROMOTED_POST_TYPES = (
    (1, "Blog post promotion"),
    (2, "Regular social post promotion"),
    (3, "Scheduled social post promotion"),
    (4, "Scheduled social post promotion")
)


class AbstractSocialPost(models.Model):
    """
    Common information about a Social Post (Abstract Model)
    Social Post = Post in Linkedin, Message in Telegram, Tweet in Twitter
    Limit of characters: Twitter: 280   Instagram: 2,200     Facebook: 63,206   Telegram: 4,400
    """

    text = models.TextField(max_length=2000)
    promote = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add = True, blank=True, null=True, editable = False)
    updated = models.DateTimeField(auto_now = True, blank=True, null=True, editable = False)
    
    promote_in_linkedin = models.BooleanField(default=True)
    promote_in_twitter = models.BooleanField(default=True)
    promote_in_telegram = models.BooleanField(default=True)
    promote_in_facebook = models.BooleanField(default=False)
    promote_in_instagram = models.BooleanField(default=False)

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
    Social Post what will be promoted in social media on a dairly basis.
    """
    promoted = models.BooleanField(default=False, editable = False)

    def __str__(self):
        return self.text




class LinkedinPost(models.Model):

    post_type = models.SmallIntegerField(null=True, blank=True, choices=SOCIAL_PROMOTED_POST_TYPES)
    linkedin_id = models.CharField(max_length=20)
    likes = models.IntegerField(null=True, blank=True)
    
    # add more fields and methods

