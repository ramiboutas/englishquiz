from __future__ import annotations

from django.test import TestCase

from .models import Contact


class ContactTest(TestCase):
    def setUp(self):
        self.contact_obj = Contact.objects.create(
            name="John",
            email="john@email.com",
            message="Hello, this is John",
        )

    def test_str_of_contact_obj(self):
        self.assertEqual(str(self.contact_obj), "John")

    def test_contact_obj_fields(self):
        self.assertEqual(self.contact_obj.name, "John")
        self.assertEqual(self.contact_obj.email, "john@email.com")
        self.assertEqual(self.contact_obj.message, "Hello, this is John")
