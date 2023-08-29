from __future__ import annotations

import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object(settings, namespace="CELERY")
app.conf.timezone = settings.TIME_ZONE
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "share_random_quiz_question": {
        "task": "socialmedia.tasks.share_random_quiz_question",
        "schedule": crontab(hour=14, minute=00),
    },
    "share_social_post": {
        "task": "socialmedia.tasks.share_social_post",
        "schedule": crontab(hour=12, minute=30),
    },
    "share_blog_post": {
        "task": "socialmedia.tasks.share_blog_post",
        "schedule": crontab(hour=8, minute=30, day_of_week="wednesday"),
    },
    "share_random_quiz_question_as_poll": {
        "task": "socialmedia.tasks.share_random_quiz_question_as_poll",
        "schedule": crontab(hour=9, minute=30),
    },
    "update_linkedin_company_page_access_token": {
        "task": "socialmedia.tasks.update_linkedin_company_page_access_token",
        "schedule": crontab(0, 0, day_of_month="1", month_of_year="1,3,5,7,9,11"),
    },
    "update_featured_books": {
        "task": "affiliates.tasks.update_featured_books",
        "schedule": crontab(hour=22, minute=42),
    },
    "send_email_newsletter": {
        "task": "core.tasks.send_email_newsletter",
        "schedule": crontab(hour=8, minute=0, day_of_week="sunday"),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")  # pragma: no cover
