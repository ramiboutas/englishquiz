from __future__ import annotations

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def blog_post_seconds(self):
        all_seconds = [post.reading_time_in_seconds for post in self.blog_posts.all()]
        return sum(all_seconds)

    @property
    def number_of_social_posts(self):
        return self.regularsocialpost_set.all().count()

    @property
    def number_of_quiz_questions(self):
        return self.question_set.all().count()

    class Meta:
        db_table = "auth_user"
