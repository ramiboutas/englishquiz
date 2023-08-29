import auto_prefetch
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

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
    image_url = models.URLField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    level = models.PositiveSmallIntegerField(default=3, choices=BOOK_LEVELS)
    test_type = models.CharField(
        default="general", max_length=16, choices=BOOK_TEST_TYPES
    )
    category = models.CharField(
        default="general", max_length=16, choices=BOOK_CATEGORIES
    )
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    affiliate_link = models.URLField(null=True)
    affiliate_label = models.CharField(max_length=64, blank=True, null=True)
    affiliate_disclosure = models.CharField(
        max_length=16, choices=DISCLOSURES, default="amazon"
    )

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
