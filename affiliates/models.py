import random

import auto_prefetch

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify

from utils.telegram import report_to_admin
from markdownx.models import MarkdownxField

AFFILIATE_REGION_SCOPE_CHOICES = (
    ("US", "USA"),
    ("DE", "Germany"),
    ("ES", "Spain"),
    ("IT", "Italy"),
    ("FR", "France"),
    ("UK", "United Kingdom"),
)


DISCLOSURES = (
    ("amazon", "As an Amazon Associate I earn from qualifying purchases."),
    ("general", "We will earn some commisions from this links"),
)


BOOK_LEVELS = (
    (1, "Very Basic"),
    (2, "Basic"),
    (3, "Intermediate"),
    (4, "Intermediate-Advanced"),
    (5, "Advanced"),
    (6, "Very Advanced"),
)


BOOK_TEST_TYPES = (
    ("general", "General 🤓"),
    ("cambridge", "Cambridge 💂‍♂️"),
    ("ielts", "IELTS 🇬🇧"),
    ("toefl", "TOEFL 🗽"),
    ("celpip", "CELPIP 🏢"),
)

BOOK_CATEGORIES = (
    ("general", "General 📗"),
    ("text-book", "Text books 📚"),
    ("writing", "Writing 📝"),
    ("vocabulary", "Vocabulary 👨‍‍🏫"),
)


class Book(auto_prefetch.Model):
    name = models.CharField(max_length=128)
    description = MarkdownxField()
    image = models.ImageField(upload_to="books", null=True)
    level = models.PositiveSmallIntegerField(default=3, choices=BOOK_LEVELS)
    test_type = models.CharField(
        default="general",
        max_length=16,
        choices=BOOK_TEST_TYPES,
    )
    category = models.CharField(
        default="general",
        max_length=16,
        choices=BOOK_CATEGORIES,
    )
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    affiliate_link = models.URLField(null=True)
    affiliate_label = models.CharField(max_length=64, blank=True, null=True)
    affiliate_disclosure = models.CharField(
        max_length=16,
        choices=DISCLOSURES,
        default="amazon",
    )
    promoted = models.BooleanField(default=False)

    def get_remote_image(self):
        from pathlib import Path
        import urllib.request
        from django.core.files import File

        if self.image_url and not self.image:
            tmpfilepath, _ = urllib.request.urlretrieve(self.image_url)
            path = Path(tmpfilepath)
            filename = path.name + "." + self.image_url.split(".")[-1]
            with path.open(mode="rb") as f:
                self.image = File(f, name=filename)
                self.save()

    def get_detail_url(self):
        return reverse("book_detail", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_list_url(self):
        return reverse("book_list")

    def get_related_books(self, n=3):
        return self.__class__.objects.exclude(pk=self.pk).filter(
            level__in=[self.level - 1, self.level, self.level + 1],
            test_type=self.test_type,
            category=self.category,
        )[:n]

    def add_view(self):
        self.views += 1
        self.save()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("-views",)

    def get_promotion_text(self):
        """
        It generates text for promoting a blog post
        """
        starting_list = [
            "Check out this book if you are interested in learning in an organized way!",
            "Have look at this book!",
            "We all know that studying with a book is one best ways to get more knowledge. We recoomend this one for boosting your English!",
        ]
        text = ""
        text += f"{random.choice(starting_list)}\n\n"
        text += f"📗 Title: {self.name}\n\n"
        text += f"📊 Level: {self.get_level_display()}\n\n"
        text += f"More here 👉 {settings.SITE_BASE_URL}{self.get_detail_url()}\n\n"

        return text

    @classmethod
    def get_random_object_to_promote(cls):
        qs = cls.objects.filter(promoted=False)
        if not qs.exists():
            qs = cls.objects.all()
            report_to_admin(f"All books were promoted, please make more.")
        return random.choice(list(qs))


class BookAffiliateLink(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    url = models.URLField()
    label = models.CharField(max_length=64)
    is_global = models.BooleanField(default=True)
    country_code = models.CharField(max_length=8)
