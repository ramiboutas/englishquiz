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

BOOK_LEVEL_CHOICES = (
    (1, "Very Basic"),
    (2, "Basic"),
    (3, "Intermediate"),
    (4, "Intermediate-Advanced"),
    (5, "Advanced"),
    (6, "Very Advanced"),
)


BOOK_TEST_TYPE_CHOICES = (
    ("general", "General 🤓"),
    ("cambridge", "Cambridge 💂‍♂️"),
    ("ielts", "IELTS 🇬🇧"),
    ("toefl", "TOEFL 🗽"),
    ("celpip", "CELPIP 🏢"),
)

BOOK_CATEGORY_CHOICES = (
    ("general", "General 📗"),
    ("text-book", "Text books 📚"),
    ("writing", "Writing 📝"),
    ("vocabulary", "Vocabulary 👨‍‍🏫"),
)


class CountryVisitor(auto_prefetch.Model):
    country_code = models.CharField(max_length=5)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.country_code

    def add_view(self):
        self.views += 1
        self.save()
    
    class Meta:
        ordering = ("-views",)

class Book(auto_prefetch.Model):
    name = models.CharField(max_length=64)
    description = MarkdownxField()
    image_url = models.URLField(blank=True, null=True)
    level = models.PositiveSmallIntegerField(default=3, choices=BOOK_LEVEL_CHOICES)
    test_type = models.CharField(default="general", max_length=16, choices=BOOK_TEST_TYPE_CHOICES)
    category = models.CharField(default="general", max_length=16, choices=BOOK_CATEGORY_CHOICES)
    slug = models.SlugField(blank=True, unique=True)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def get_detail_url(self):
        return reverse("book_detail", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_list_url(self):
        return reverse("book_list")

    def get_related_books(self, n=3):
        return self.__class__.objects.exclude(pk=self.pk).filter(
            level=self.level,
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

    class Meta:
        ordering = ("-views",)



class BookAffiliateLink(auto_prefetch.Model):
    book = auto_prefetch.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="affiliate_links"
    )
    url = models.URLField()
    label = models.CharField(max_length=64, blank=True, null=True)
    is_global = models.BooleanField(default=False)
    country_code = models.CharField(
        max_length=2, choices=AFFILIATE_REGION_SCOPE_CHOICES
    )

    def __str__(self):
        return self.url
