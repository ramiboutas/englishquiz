from email import message
from django.conf import settings
from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from slugger import AutoSlugField


class Contact(models.Model):
    name        = models.CharField(max_length=50)
    email       = models.EmailField()
    message     = models.TextField(max_length=250)
    response    = models.TextField(max_length=250, null=True, blank=True)
    created     = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class FlexPage(models.Model):

    title       = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    public      = models.BooleanField(default=False)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="flexpages")
    slug        = AutoSlugField(populate_from='title')
    content     = MarkdownxField()
    
    views       = models.PositiveIntegerField(default=0)
        
    created     = models.DateField(auto_now_add=True)
    updated     = models.DateField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_postdetail", kwargs={"slug": self.slug, "level": self.level})
    
    def get_detail_url(self):
        return self.get_absolute_url()
    
    def add_view(self):
        self.views += 1
        self.save()