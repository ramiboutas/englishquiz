from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Quiz, Lection
from socialmedia import tasks as socialmedia_tasks



# THIS MAKES PROBLEMS: IT GENERATES MULTIPLE TASK INSTANCE
# @receiver(post_save, sender=Quiz)
# def schedule_promoting_quiz(sender, instance, **kwargs):
#     """
#     Schedules a quiz that is set for promoting in social media
#     """
#     if instance.promote and not instance.promoted:
#         socialmedia_tasks.promote_quiz_instance.apply_async(eta=instance.promote_date,
#                                                             expires=1, kwargs={"pk":instance.pk})
#
#
#
# @receiver(post_save, sender=Lection)
# def schedule_promoting_lection(sender, instance, **kwargs):
#     """
#     Schedules a lection that is set for promoting in social media
#     """
#     if instance.promote and not instance.promoted:
#         socialmedia_tasks.promote_lection_instance.apply_async(eta=instance.promote_date,
#                                                                 expires=1, kwargs={"pk":instance.pk})
