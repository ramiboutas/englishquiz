from wagtail.signals import page_published

from django.dispatch import receiver

from puput.models import EntryPage

from .tasks import (promote_post_instance_in_telegram,
                    promote_post_instance_in_linkedin,
                    promote_post_instance_in_twitter)

@receiver(page_published, sender=EntryPage)
def post_in_social_media(sender, instance, *args, **kwargs):
    promote_in_telegram = True
    promote_in_linkedin = True
    promote_in_twitter = True

    if promote_in_telegram:
        promote_post_instance_in_telegram(instance)

    if promote_in_linkedin:
        promote_post_instance_in_linkedin(instance)

    if promote_in_twitter:
        promote_post_instance_in_twitter(instance)
