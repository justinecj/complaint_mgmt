from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('ADMIN', 'Admin'),
    ('EMPLOYEE', 'Employee'),
)

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
