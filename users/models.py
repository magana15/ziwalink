from django.db import models
from django.contrib.auth.models import AbstractUser


class ZiwaUser(AbstractUser):
    class Role(models.TextChoices):
        FARMER = "FARMER", "Farmer"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.FARMER,
    )

    phone_number = models.CharField(

        max_length=20,
        blank=True,
        null=True
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    def is_farmer(self):
        return self.role == self.Role.FARMER
    def is_admin(self):
        return self.role == self.Role.ADMIN
    def __str__(self):
        return f"{self.username} ({self.role})"
