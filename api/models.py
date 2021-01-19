from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name="Категория",
                            blank=True)
    slug = models.SlugField(unique=True, verbose_name="Slug")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name="Жанр",
                            blank=True)
    slug = models.SlugField(unique=True, verbose_name="Slug")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    year = models.IntegerField(validators=[
        MaxValueValidator(2022),
        MinValueValidator(1)
    ],
        blank=True, verbose_name="Год выпуска", db_index=True
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    genre = models.ManyToManyField(Genre,
                                   through="GenreTitle",
                                   verbose_name="Жанр")
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name="Категория",
                                 related_name="titles")

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(Title,
                              verbose_name="Произведение",
                              on_delete=models.CASCADE,
                              related_name="reviews")
    text = models.TextField(verbose_name="Текст оценки",)
    author = models.ForeignKey(User,
                               verbose_name="Автор",
                               on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.PositiveSmallIntegerField(validators=[
                                    MaxValueValidator(10),
                                    MinValueValidator(1)
                                ],
                                verbose_name="Оценка",
                                help_text="Оценка от 0 до 10",
                                )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "author"],
                                    name="unique_review"),
        ]
        ordering = ("-pub_date",)
        verbose_name = "Обзор"
        verbose_name_plural = "Обзоры"


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               verbose_name="Обзор",
                               on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField(verbose_name="Текст коментария",)
    author = models.ForeignKey(User,
                               verbose_name="Автор",
                               on_delete=models.CASCADE,
                               related_name="comments")
    pub_date = models.DateTimeField("Дата добавления",
                                    auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
