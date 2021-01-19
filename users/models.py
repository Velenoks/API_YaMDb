from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class User(AbstractUser):
    bio = models.TextField(
        max_length=300,
        blank=True,
        verbose_name='О пользователе'
    )
    role = models.CharField(
        max_length=10,
        blank=False,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name='Роль пользователя'
    )
    email = models.EmailField(
        unique=True,
        db_index=True,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name='Имя пользователе'
    )

    class Meta:
        ordering = ['-id']
