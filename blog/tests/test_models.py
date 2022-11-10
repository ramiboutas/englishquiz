from __future__ import annotations

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
        self.post = BlogPost.objects.create(
            title="Test title", created_by=self.user, content="This is my content"
        )

    def test_post_title(self):
        self.assertEqual(self.post.title, "Test title")

    def test_post_slug(self):
        self.assertEqual(self.post.slug, "test-title")

    def test_post_author(self):
        self.assertEqual(self.post.created_by, self.user)

    def test_post_content(self):
        self.assertEqual(self.post.content, "This is my content")
