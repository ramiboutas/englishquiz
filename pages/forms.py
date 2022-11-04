from __future__ import annotations

from captcha.fields import CaptchaField
from django.forms import ModelForm

from .models import Contact


# Create the form class.
class ContactForm(ModelForm):
    # add https://django-simple-captcha.readthedocs.io/en/latest/usage.html
    captcha = CaptchaField()

    class Meta:
        model = Contact
        fields = ["name", "email", "message", "subscribe"]
