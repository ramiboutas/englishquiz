from __future__ import annotations

from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin

from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.models import BlogPost

User = get_user_model()

def get_model_fields(model):
    return [field.name for field in model._meta.get_fields()]


class MockRequest:
    pass

class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True

request = MockRequest()
request.user = MockSuperUser()


class AdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_modeladmin_str(self):
        ma = ModelAdmin(BlogPost, self.site)
        self.assertEqual(str(ma), "blog.ModelAdmin")

    def test_default_fields(self):
        ma = ModelAdmin(BlogPost, self.site)
        self.assertEqual(
            list(ma.get_form(request).base_fields), get_model_fields(BlogPost)
        )
        # self.assertEqual(list(ma.get_fields(request)), ["name", "bio", "sign_date"])
        # self.assertEqual(
        #     list(ma.get_fields(request, self.band)), ["name", "bio", "sign_date"]
        # )
        # self.assertIsNone(ma.get_exclude(request, self.band))
