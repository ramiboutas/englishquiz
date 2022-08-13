from django.conf import settings
from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from slugger import AutoSlugField


from taggit.managers import TaggableManager

class BlogPost(models.Model):
    DIFFICULTY_LEVEL = [
        ("elementary", "Elementary"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advamced"),
        ("general", "General"),
    ]

    
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    level = models.CharField(choices=DIFFICULTY_LEVEL, default="general", max_length=30)
    tags = TaggableManager()
    public = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    slug = AutoSlugField(populate_from='title')
    content = MarkdownxField()
    
    views = models.PositiveIntegerField(default=0)
    
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_postdetail", kwargs={"slug": self.slug, "level": self.level})
    
    @classmethod
    def get_last_posts(cls, post_count=10):
        return cls.objects.filter(public=True).order_by('-created')[:post_count]
    
    @classmethod
    def get_popular_posts(cls, post_count=4):
        return cls.objects.filter(public=True).order_by('-views')[:post_count]

    @classmethod
    def get_all_posts(cls):
        return cls.objects.all().order_by('-created')
    
    def add_view(self):
        self.views += 1
        self.save()
