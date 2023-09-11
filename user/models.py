from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STATUS_CHOICES = (
        ("rest_rep", "Restaurant representative"),
        ("employee", "Employee"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
