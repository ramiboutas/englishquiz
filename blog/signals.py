from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BlogPost
from .tasks import create_blog_post_pdf


@receiver(post_save, sender=BlogPost)
def trigger_blog_post_pdf_creation(sender, instance, **kwargs):
    """
    It triggers the creation of a pdf file from a blog post instance
    """
    # We refresh from db to avoid multiple calls to the task create_blog_post_pdf
    instance.refresh_from_db()

    if instance.public and not instance.pdf_created:
        create_blog_post_pdf.apply_async(countdown=1, kwargs={"pk": instance.pk})
