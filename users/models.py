from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    whatever = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "auth_user"
