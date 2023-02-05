from __future__ import annotations

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object(settings, namespace="CELERY")
app.conf.timezone = settings.TIME_ZONE

# Not needed: https://github.com/celery/celery/issues/3341
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "share_random_question": {
        "task": "socialmedia.tasks.share_random_question_instance",
        "schedule": crontab(hour="10, 15", minute=00),
    },
    "share_regular_social_post": {
        "task": "socialmedia.tasks.share_regular_social_post",
        "schedule": crontab(hour=12, minute=30),  # when more instances available: add crontab(hour='8,13', minute=00)
    },
    "like_recent_tweets": {
        "task": "socialmedia.tasks.like_recent_tweets",
        "schedule": crontab(minute=26),
    },
    "share_random_question_as_poll": {
        "task": "socialmedia.tasks.share_random_question_as_poll",
        "schedule": crontab(hour="11, 19", minute=30),
    },
    "update_featured_books": {
        "task": "affiliates.tasks.update_featured_books",
        "schedule": crontab(hour=20, minute=50),
    },
    "send_email_newsletter": {
        "task": "send_email_newsletter_task",
        "schedule": crontab(minute=0, hour="8"),
    },
    "delete_responded_contact_instances": {
        "task": "delete_responded_contact_instances",
        "schedule": crontab(hour=3, minute=00),
    },
    "update_linkedin_company_page_access_token": {
        "task": "update_linkedin_company_page_access_token",
        "schedule": crontab(0, 0, day_of_month="1", month_of_year="1,3,5,7,9,11"),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")  # pragma: no cover
