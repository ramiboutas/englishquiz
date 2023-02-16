from django.db import models




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