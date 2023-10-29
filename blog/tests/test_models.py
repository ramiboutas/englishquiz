from __future__ import annotations

import readtime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from blog.models import BlogPost

User = get_user_model()


class BlogModelTests(TestCase):
    """
    Testing the BlogPost model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="test-user", password="test-password"
        )
        self.blogpost_content = """
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        when an unknown printer took a galley of type and scrambled it to make a type specimen book.
        It has survived not only five centuries, but also the leap into electronic typesetting,
        remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset
        sheets containing Lorem Ipsum passages, and more recently with desktop publishing software
         like Aldus PageMaker including versions of Lorem Ipsum.
        """
        self.post = BlogPost.objects.create(
            title="Test title",
            description="This is my description",
            created_by=self.user,
            public=True,
            content=self.blogpost_content,
        )

        self.yesterday_post = BlogPost.objects.create(
            title="Post from yesteday",
            description="This is my description",
            created_by=self.user,
            public=True,
            content=self.blogpost_content,
            views=100,
            created=timezone.now() - timezone.timedelta(days=1),
        )

        self.last_week_post = BlogPost.objects.create(
            title="Post from last week",
            description="This is my description",
            created_by=self.user,
            content=self.blogpost_content,
            public=True,
            views=10,
            created=timezone.now() - timezone.timedelta(weeks=1),
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

    def test_absolute_and_detail_url(self):
        target_url = "/blog/test-title/"
        self.assertEqual(self.post.get_absolute_url(), target_url)
        self.assertEqual(self.post.get_detail_url(), target_url)

    def test_last_posts_cls_method(self):
        last_posts = self.post.__class__.get_last_posts()
        self.assertEqual(last_posts.count(), 3)
        self.assertEqual(last_posts[0], self.post)
        self.assertEqual(last_posts[1], self.yesterday_post)
        self.assertEqual(last_posts[2], self.last_week_post)

    def test_popular_posts_cls_method(self):
        popular_posts = self.post.__class__.get_popular_posts()
        self.assertEqual(popular_posts.count(), 3)
        self.assertEqual(popular_posts[0], self.yesterday_post)
        self.assertEqual(popular_posts[1], self.last_week_post)
        self.assertEqual(popular_posts[2], self.post)

    def test_get_all_posts(self):
        all_posts = self.post.__class__.get_all_posts()
        self.assertEqual(all_posts.count(), 3)
        self.assertIn(self.post, all_posts)
        self.assertIn(self.yesterday_post, all_posts)
        self.assertIn(self.last_week_post, all_posts)

    def test_add_view(self):
        self.post.add_view()
        self.assertEqual(self.post.views, 1)

    def test_get_meta_description(self):
        meta_description = self.post.get_meta_description()
        self.assertEqual(meta_description, "This is my description")

    def test_get_meta_keywords(self):
        meta_keywords = self.post.get_meta_keywords()
        self.assertIsInstance(meta_keywords, str)
        self.assertGreater(len(meta_keywords), 1)
        self.assertTrue("," in meta_keywords)

    def test_get_meta_title(self):
        title = self.post.get_meta_title()
        self.assertEqual(title, "Test title")
