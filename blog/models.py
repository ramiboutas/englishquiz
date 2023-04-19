from __future__ import annotations

import auto_prefetch
import readtime
from django.conf import settings
from django.db import models
from django.urls import reverse
from slugger import AutoSlugField
from taggit.managers import TaggableManager

from markdownx.models import MarkdownxField
from utils.keywords import get_keywords_from_text


class BlogPost(auto_prefetch.Model):
    DIFFICULTY_LEVEL = [
        ("elementary", "Elementary"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("general", "General"),
    ]

    title = models.CharField(max_length=70)
    description = models.TextField(blank=False, null=True)
    level = models.CharField(
        choices=DIFFICULTY_LEVEL,
        default="general",
        max_length=30,
    )
    tags = TaggableManager()
    public = models.BooleanField(default=False)
    created_by = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="blog_posts",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    slug = AutoSlugField(populate_from="title")
    content = MarkdownxField()
    pdf = models.FileField(
        upload_to="blog-posts/%Y/%m/%d",
        blank=True,
        null=True,
    )
    create_pdf = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    promoted = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("-created",)

    @property
    def reading_time(self):
        return readtime.of_markdown(self.content).minutes

    @property
    def reading_time_in_seconds(self):
        return readtime.of_markdown(self.content).seconds

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog_postdetail", kwargs={"slug": self.slug, "level": self.level}
        )

    def get_detail_url(self):
        return self.get_absolute_url()

    @classmethod
    def get_last_posts(cls, post_count=10):
        return cls.objects.filter(public=True).order_by("-created")[:post_count]

    @classmethod
    def get_popular_posts(cls, post_count=4):
        return cls.objects.filter(public=True).order_by("-views")[:post_count]

    @classmethod
    def get_all_posts(cls):
        return cls.objects.all().order_by("-created")

    def add_view(self):
        self.views += 1
        self.save()

    def get_meta_description(self):
        return self.description[0:160]

    def get_meta_keywords(self):
        return get_keywords_from_text(self.content)

    def get_meta_title(self):
        return self.title
