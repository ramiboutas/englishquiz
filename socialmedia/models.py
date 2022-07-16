from django.db import models


TWIITER_USERNAME = 'EnglishstuffOn'

####################################
### Sending to social media APIs ###
####################################

class AbstractSocialPost(models.Model):
    """
    Common information about a Social Post (Abstract Model)
    Social Post = Post in Linkedin, Message in Telegram, Tweet in Twitter
    Limit of characters: Twitter: 280   Instagram: 2,200     Facebook: 63,206   Telegram: 4,400
    """
    
    text                    = models.TextField(max_length=2000)
    image                   = models.ImageField(upload_to='socialposts/', null=True, blank=True)
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




        return LinkedinPost.objects.create(
            urn_li_share  = json.loads(response.text)["id"],
            text            = text,
            response_text = response.text
        )


#########################################
### Retrieving from social media APIs ###
#########################################


class LinkedinPost(models.Model):
    urn_li_share        = models.CharField(max_length=50)
    text                = models.TextField(max_length=1000)
    date             = models.DateTimeField(auto_now_add = True, blank=True, null=True, editable = False)
    # Insights
    click_count         = models.PositiveIntegerField(null=True)
    comment_count       = models.PositiveIntegerField(null=True)
    engagement          = models.FloatField(null=True)
    impression_count    = models.PositiveIntegerField(null=True)
    like_count          = models.PositiveIntegerField(null=True)
    share_count         = models.PositiveIntegerField(null=True)
    api_delete  = models.BooleanField(verbose_name="Delete from Linkedin", default=False, help_text="It gets deleted after clicking on Save")
    api_deleted = models.BooleanField(verbose_name="Already deleted from Linkedin", default=False)

    def __str__(self) -> str:
        return self.text[:100]


class TelegramMessage(models.Model):
    chat_id     = models.BigIntegerField()
    message_id  = models.BigIntegerField()
    link        = models.CharField(max_length=100)
    text        = models.TextField(max_length=4000)
    date        = models.DateTimeField()
    api_delete  = models.BooleanField(verbose_name="Delete from Telegram", default=False, help_text="It gets deleted after clicking on Save")    
    api_deleted = models.BooleanField(verbose_name="Already deleted from Telegram", default=False)

    def __str__(self) -> str:
        return self.text[:100]


class Tweet(models.Model):
    twitter_id      = models.PositiveIntegerField()
    id_str          = models.CharField(max_length=30)
    text            = models.TextField(max_length=300)
    twitter_url     = models.URLField(null=True)
    created_at      = models.DateTimeField()
    retweet_count   = models.PositiveIntegerField()
    favorite_count  = models.PositiveIntegerField()
    api_delete  = models.BooleanField(verbose_name="Delete from Twitter", default=False, help_text="It gets deleted after clicking on Save")
    api_deleted = models.BooleanField(verbose_name="Already deleted from Twitter", default=False)

    def __str__(self) -> str:
        return self.text[:100]
    
    def save(self, *args, **kwargs):
        self.twitter_url = f"https://twitter.com/{TWIITER_USERNAME}/status/{self.id_str}"
        super(Tweet, self).save(*args, **kwargs)






class SocialMediaPostedItem(models.Model):
    
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
