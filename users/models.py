from __future__ import annotations

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def blog_post_seconds(self):
        all_seconds = [post.reading_time_in_seconds for post in self.blog_posts.all()]
        return sum(all_seconds)

    @property
    def social_posts(self):
        return self.socialpost_set.all().count()

    @property
    def quiz_questions(self):
        return self.question_set.all().count()

    @property
    def total_euros(self):
        euros_list = [
            0.03 * self.blog_post_seconds,  # 0.03 €/second
            0.5 * self.social_posts,  # 0.50 € / social post
            0.5 * self.quiz_questions,  # 0.50 € / quiz question
        ]
        return sum(euros_list)

    class Meta:
        db_table = "auth_user"
