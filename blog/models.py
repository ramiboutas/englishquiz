from django.conf import settings
from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from slugger import AutoSlugField


from taggit.managers import TaggableManager

class BlogPost(models.Model):
    DIFFICULTY_LEVEL = [
        (1, "BEGINNER"),
        (2, "INTERMEDIATE"),
        (3, "ADVANCED"),
    ]

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    level = models.PositiveSmallIntegerField(choices=DIFFICULTY_LEVEL, default=1)
    tags = TaggableManager()
    public = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    slug = AutoSlugField(populate_from='title')
    
    content = MarkdownxField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})



