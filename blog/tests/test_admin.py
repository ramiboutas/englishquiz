from __future__ import annotations

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.admin import BlogPostAdmin
from blog.models import BlogPost

User = get_user_model()


class MockRequest:
    def __init__(self, user=None):
        self.user = user


class BlogAdminTests(TestCase):
    def setUp(self, *args, **kwargs):
        self.site = AdminSite()
        super().__init__(*args, **kwargs)

    def test_modeladmin_str(self):
        ma = ModelAdmin(BlogPost, self.site)
        self.assertEqual(str(ma), "blog.ModelAdmin")

    def test_post_author(self):
        superuser = User.objects.create_superuser(
            username="super", email="super@email.org", password="pass"
        )
        request = MockRequest()
        request.user = superuser

        obj = BlogPost(
            title="Testing title",
            description="He comes my description",
            tags="tag",
            content="here comes my content in ##Markdown",
        )
        ma = BlogPostAdmin(BlogPost, self.site)
        ma.save_model(
            obj=obj, request=MockRequest(user=superuser), form=None, change=None
        )

        self.assertEqual(BlogPost.objects.count(), 1)
        post = BlogPost.objects.all()[0]
        self.assertEqual(post.title, "Testing title")
        self.assertEqual(post.created_by, superuser)
