import auto_prefetch
from markdownx.models import MarkdownxField

from django.db import models
from django.urls import reverse
from django.utils.text import slugify



BOOK_LEVEL_CHOICES = (
    (None, "Not applicable"),
    ("a1", "A1"),
    ("a2", "A2"),
    ("b1", "B1"),
    ("b2", "B2"),
    ("c1", "C1"),
    ("c2", "C2"),
)

AFFILIATE_REGION_SCOPE_CHOICES = (
    ("US", "USA"),
    ("DE", "Germany"),
    ("ES", "Spain"),
    ("FR", "France"),
    ("IT", "Italy"),
)


class Book(auto_prefetch.Model):
    name = models.CharField(max_length=64)
    description = MarkdownxField()
    image_url = models.URLField(blank=True, null=True)
    level = models.CharField(max_length=2, null=True, blank=True, default="b2", choices=BOOK_LEVEL_CHOICES)
    slug = models.SlugField(blank=True, unique=True)
    featured = models.BooleanField(default=False)

    def get_detail_url(self):
        return reverse("book_detail", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_list_url(self):
        return reverse("book_list")

    def get_related_books(self):
        pass
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class BookAffiliateLink(auto_prefetch.Model):
    book = auto_prefetch.ForeignKey(Book, on_delete=models.CASCADE, related_name="affiliate_links")
    label = models.CharField(max_length=64)
    url = models.URLField()
    is_global = models.BooleanField(default=False)
    country_code = models.CharField(max_length=2, choices=AFFILIATE_REGION_SCOPE_CHOICES)

    def __str__(self):
        return self.url