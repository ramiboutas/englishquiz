from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Quiz, Lection
from socialmedia import tasks as socialmedia_tasks


@receiver(post_save, sender=Quiz)
def schedule_promoting_quiz(sender, instance, **kwargs):
    """
    Schedules a quiz that is set for promoting in social media
    """
    if instance.promote:
        socialmedia_tasks.promote_quiz_instance.apply_async(eta=instance.promote_date,
                                                            kwargs={"pk":instance.pk})



@receiver(post_save, sender=Lection)
def schedule_promoting_lection(sender, instance, **kwargs):
    """
    Schedules a lection that is set for promoting in social media
    """
    if instance.promote:
        socialmedia_tasks.promote_lection_instance.apply_async(eta=instance.promote_date,
                                                                kwargs={"pk":instance.pk})
