from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class User(AbstractUser):
    bio = models.TextField(max_length=300, blank=True)
    role = models.CharField(
        max_length=10,
        blank=False,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name='Роль пользователя'
    )
    email = models.EmailField('email', unique=True)
    confirmation_code = models.UUIDField(null=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
    )
