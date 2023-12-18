import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-date_joined"]
        indexes = [
            models.Index(
                fields=[
                    "guid",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.email} - {self.guid.hex}"


class MedEasyBaseModel(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    created = models.DateTimeField(default=timezone.now, editable=False)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True