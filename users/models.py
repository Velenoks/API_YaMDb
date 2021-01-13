from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(max_length=300)
    USER_ROLES = ['admin', 'moderator', 'user']
    role = models.CharField(blank=False, choices=USER_ROLES, default='user')
