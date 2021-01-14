from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(validators=[
        MaxValueValidator(2022),
        MinValueValidator(1)
    ],
        blank=True
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="titles")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-year',)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class Review(models.Model):
    title = models.ForeignKey(Titles, null=False, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    score = models.IntegerField(validators=[
                                    MaxValueValidator(100),
                                    MinValueValidator(1)
                                ]
                                )
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Обзор"
        verbose_name_plural = "Обзоры"


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField("created", auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class GenreTitle(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE, related_name="genres")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="titles")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "genre"],
                                    name="unique_connection"),
        ]
