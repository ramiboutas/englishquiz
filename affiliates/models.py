import auto_prefetch
from django.db import models
from django.urls import reverse
from django.utils.text import slugify



BOOK_LEVEL_CHOICES = (
    ("a1", "A1"),
    ("a2", "A2"),
    ("b1", "B1"),
    ("b2", "B2"),
    ("c1", "C1"),
    ("c2", "C2"),
)

AFFILIATE_REGION_SCOPE_CHOICES = (
    ("global", "Global"),
    ("US", "USA"),
    ("DE", "Germany"),
    ("ES", "Spain"),
    ("FR", "France"),
    ("IT", "Italy"),
)



class Book(auto_prefetch.Model):
    name = models.CharField(max_length=64)
    level = models.CharField(max_length=2, default="b2", choices=BOOK_LEVEL_CHOICES)
    slug = models.SlugField(blank=True, unique=True)
    featured = models.BooleanField(default=False)

    def get_detail_url(self):
        return reverse("book_detail", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_list_url(self):
        return reverse("quiz_list")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class BookAffiliateLink(auto_prefetch.Model):
    book = auto_prefetch.ForeignKey(Book, on_delete=models.CASCADE)
    url = models.URLField()
    region = models.CharField(max_length=6, choices=AFFILIATE_REGION_SCOPE_CHOICES)

    def __str__(self):
        return self.url