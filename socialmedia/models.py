from django.db import models

# Create your models here.

class AbstractSocialPost(models.Model):
    """
    Common information about a Social Post (Abstract Model)
    Social Post = Post in Linkedin, Message in Telegram, Tweet in Twitter
    Limit of characters: Twitter: 280   Instagram: 2,200     Facebook: 63,206   Telegram: 4,400
    """

    text = models.TextField(max_length=280)
    promote = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ScheduledSocialPost(AbstractSocialPost):
    """
    Social Post what will be promoted in social media on a specific data and time.
    """
    promote_date = models.DateTimeField()

    def __str__(self):
        return self.text[:100]


class RegularSocialPost(AbstractSocialPost):
    """
    Social Post what will be promoted in social media on a dairly basis.
    """
    promoted = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:100]


class AbstractLargeSocialPost(models.Model):
    """
    Common information about a Large Social Post (Abstract Model)
    Limit of characters: Twitter: 280   Instagram: 2,200     Facebook: 63,206   Telegram: 4,400
    """

    text = models.TextField(max_length=2000)
    promote = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ScheduledLargeSocialPost(AbstractLargeSocialPost):
    """
    Large Social Post what will be promoted in social media on a specific data and time.
    """
    promote_date = models.DateTimeField()

    def __str__(self):
        return self.text[:100]


class LargeSocialPost(AbstractLargeSocialPost):
    """
    Large Social Post what will be promoted in social media on a dairly basis.
    """
    promoted = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:100]
