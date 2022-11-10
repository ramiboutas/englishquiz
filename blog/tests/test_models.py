from __future__ import annotations

import readtime
from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.models import BlogPost

User = get_user_model()


class BlogPostModelTest(TestCase):
    """
    Testing the BlogPost model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="test-user", password="test-password"
        )
        self.blogpost_content = """
        hello adfadsfadsf dfasd dfasdadsagads asdf
        asdasdfsgsadf dsafsgadsfasg fasd
        agadsg
        asgadsggasgasfgasdgasdfgasg sdgasdg sdasdfa
        """
        self.post = BlogPost.objects.create(
            title="Test title",
            created_by=self.user,
            content=self.blogpost_content,
        )

    def test_post_str(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_post_title(self):
        self.assertEqual(self.post.title, "Test title")

    def test_post_slug(self):
        self.assertEqual(self.post.slug, "test-title")

    def test_post_author(self):
        self.assertEqual(self.post.created_by, self.user)

    def test_post_content(self):
        self.assertEqual(self.post.content, self.blogpost_content)

    def test_reading_time(self):
        post_mins = self.post.reading_time
        post_secs = self.post.reading_time_in_seconds
        self.assertEqual(post_mins, readtime.of_markdown(self.blogpost_content).minutes)
        self.assertEqual(post_secs, readtime.of_markdown(self.blogpost_content).seconds)
