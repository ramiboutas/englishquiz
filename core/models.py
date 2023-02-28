from __future__ import annotations

import auto_prefetch
from django.conf import settings
from django.db import models
from django.urls import reverse
from slugger import AutoSlugField

from markdownx.models import MarkdownxField


class FlexPage(auto_prefetch.Model):
    """
    Definition of a FlexPage object
    """

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=False)
    created_by = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="flexpages",
    )
    slug = AutoSlugField(populate_from="title")
    content = MarkdownxField()
    views = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "core_flexpage",
            kwargs={
                "slug": self.slug,
            },
        )

    def get_detail_url(self):
        return self.get_absolute_url()

    def add_view(self):
        self.views += 1
        self.save()


class CountryVisitor(models.Model):
    country_code = models.CharField(max_length=5)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.country_code

    def add_view(self):
        self.views += 1
        self.save()

    class Meta:
        ordering = ("-views",)


class Contact(auto_prefetch.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField(max_length=250)
    response = models.TextField(max_length=250, null=True, blank=True)
    responded = models.BooleanField(default=False)
    responded_on = models.DateField(null=True, blank=True)
    responded_by = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    subscribe = models.BooleanField(
        verbose_name="Subscribe to our Newsletter", default=False
    )
    subscribed = models.BooleanField(default=False)

    created_on = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        not_allowed_strings = ["http://", "https://", "www.", "money", "$", "€"]
        if not any(x in self.message for x in not_allowed_strings):
            super().save(*args, **kwargs)
