from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, blank=False, primary_key=True, unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.username
