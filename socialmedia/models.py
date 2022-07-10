from pyexpat import model
from django.db import models


# Create your models here.

SOCIAL_PROMOTED_POST_TYPES = (
    (1, "Blog post promotion"),
    (2, "Regular social post promotion"),
    (3, "Scheduled social post promotion"),
    (4, "Scheduled social post promotion")
)


TWIITER_USERNAME = 'EnglishstuffOn'


class AbstractSocialPost(models.Model):
    """
    Common information about a Social Post (Abstract Model)
    Social Post = Post in Linkedin, Message in Telegram, Tweet in Twitter
    Limit of characters: Twitter: 280   Instagram: 2,200     Facebook: 63,206   Telegram: 4,400
    """
    
    text                    = models.TextField(max_length=2000)
    image_text              = models.TextField(max_length=200, null=True, blank=True) # if instance is null -> it cannot be promoted in instagram 
    promote_in_linkedin     = models.BooleanField(verbose_name="Promote in Linkedin", default=True)
    promote_in_twitter      = models.BooleanField(verbose_name="Promote in Twitter", default=True)
    promote_in_telegram     = models.BooleanField(verbose_name="Promote in Telegram", default=True)
    promote_in_facebook     = models.BooleanField(verbose_name="Promote in Facebook", default=False)
    promote_in_instagram    = models.BooleanField(verbose_name="Promote in Instagram", default=False)
    created                 = models.DateTimeField(auto_now_add = True, blank=True, null=True, editable = False)
    updated                 = models.DateTimeField(auto_now = True, blank=True, null=True, editable = False)

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
    post_type       = models.SmallIntegerField(null=True, blank=True, choices=SOCIAL_PROMOTED_POST_TYPES)
    linkedin_id     = models.CharField(max_length=20, null=True, blank=True)
    likes           = models.IntegerField(null=True, blank=True)
    
    # add more fields and methods

class TelegramMessage(models.Model):
    chat_id     = models.IntegerField()
    message_id  = models.IntegerField()
    link        = models.CharField(max_length=50)
    text        = models.TextField(max_length=4000)
    date        = models.DateTimeField()

    api_delete  = models.BooleanField(verbose_name="Delete from Telegram", default=False, help_text="It gets deleted from Telegram after clicking on Save")
    api_deleted = models.BooleanField(verbose_name="Already deleted from Telegram", default=False)

    def __str__(self) -> str:
        return self.text[:100]



class Tweet(models.Model):
    created_at      = models.DateTimeField()
    favorite_count  = models.IntegerField()
    twitter_id      = models.IntegerField()
    id_str          = models.CharField(max_length=30)
    retweet_count   = models.IntegerField()
    text            = models.TextField(max_length=280)

    twitter_url     = models.URLField(null=True)

    api_delete  = models.BooleanField(verbose_name="Delete from Twitter", default=False, help_text="It gets deleted from Twitter after clicking on Save")
    api_deleted = models.BooleanField(verbose_name="Already deleted from Twitter", default=False)
    
    def __str__(self) -> str:
        return self.text[:100]
    
    def save(self, *args, **kwargs):
        self.twitter_url = f"https://twitter.com/{TWIITER_USERNAME}/status/{self.id_str}"
        super(Tweet, self).save(*args, **kwargs)






class SocialMediaPostedItem(models.Model):
    # COMBINE ALL 
    post_type       = models.SmallIntegerField(null=True, blank=True, choices=SOCIAL_PROMOTED_POST_TYPES)
    
    # Linedin
    linkedin_id     = models.CharField(max_length=20, null=True, blank=True)
    linkedin_likes  = models.IntegerField(null=True, blank=True)
    
    # Instagram
    instagram_id    = models.CharField(max_length=20, null=True, blank=True)
    linkedin_likes  = models.IntegerField(null=True, blank=True)

    # Telegram
    telegram_id    = models.CharField(max_length=20, null=True, blank=True)
    telegram_likes  = models.IntegerField(null=True, blank=True)

    # Twitter
    tweet    = models.CharField(max_length=20, null=True, blank=True)
    twitter_likes  = models.IntegerField(null=True, blank=True)

    # Facebook
    facebook_id    = models.CharField(max_length=20, null=True, blank=True)    
    facebook_likes  = models.IntegerField(null=True, blank=True)
    
    # add more fields and methods
